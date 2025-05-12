#include "geobuf/geobuf.hpp"
#include "geobuf/pbf_decoder.cpp"

#include <array>
#include <mapbox/geojson_impl.hpp>
#include <mapbox/geojson_value_impl.hpp>
#include <set>

#include "rapidjson/error/en.h"
#include "rapidjson/filereadstream.h"
#include "rapidjson/filewritestream.h"
#include "rapidjson/prettywriter.h"
#include "rapidjson/stringbuffer.h"
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>

#include "spdlog/spdlog.h" // fmt::format
// fix exposed macro 'GetObject' from wingdi.h (included by spdlog.h) under
// windows, see https://github.com/Tencent/rapidjson/issues/1448
#ifdef GetObject
#undef GetObject
#endif

#include <cmath>
#include <protozero/pbf_builder.hpp>
#include <protozero/pbf_reader.hpp>

// https://github.com/mapbox/geobuf/blob/master/encode.js
// https://github.com/mapbox/geobuf/blob/master/decode.js

#ifdef NDEBUG
#define dbg(x) x
#else
#define DBG_MACRO_NO_WARNING
#include "dbg.h"
#endif

constexpr const auto RJFLAGS = rapidjson::kParseDefaultFlags |      //
                               rapidjson::kParseCommentsFlag |      //
                               rapidjson::kParseFullPrecisionFlag | //
                               rapidjson::kParseTrailingCommasFlag;
constexpr uint32_t dimXY = 2;
constexpr uint32_t dimXYZ = 3;

using RapidjsonDocument = mapbox::geojson::rapidjson_document;
using RapidjsonAllocator = mapbox::geojson::rapidjson_allocator;

namespace mapbox
{
namespace geobuf
{
// note that fp will be closed from inside after reading!
static RapidjsonValue load_json(FILE *fp)
{
    char readBuffer[65536];
    rapidjson::FileReadStream is(fp, readBuffer, sizeof(readBuffer));
    RapidjsonDocument d;
    d.ParseStream<RJFLAGS>(is);
    fclose(fp);

    // https://github.com/Tencent/rapidjson/issues/380
    return RapidjsonValue{std::move(d.Move())};
}
RapidjsonValue load_json(const std::string &path)
{
    FILE *fp = fopen(path.c_str(), "rb");
    if (!fp) {
        return {};
    }
    return load_json(fp);
}
RapidjsonValue load_json() { return load_json(stdin); }

// note that fp will be closed from inside after writing!
bool dump_json(FILE *fp, const RapidjsonValue &json, bool indent,
               bool _sort_keys)
{
    if (_sort_keys) {
        auto sorted = sort_keys(json);
        return dump_json(fp, sorted, indent, false);
    }
    using namespace rapidjson;
    char writeBuffer[65536];
    FileWriteStream os(fp, writeBuffer, sizeof(writeBuffer));
    bool succ = false;
    if (indent) {
        PrettyWriter<FileWriteStream> writer(os);
        succ = json.Accept(writer);
    } else {
        Writer<FileWriteStream> writer(os);
        succ = json.Accept(writer);
    }
    fclose(fp);
    return succ;
}

bool dump_json(const std::string &path, const RapidjsonValue &json, bool indent,
               bool sort_keys)
{
    FILE *fp = fopen(path.c_str(), "wb");
    if (!fp) {
        return false;
    }
    return dump_json(fp, json, indent, sort_keys);
}

bool dump_json(const RapidjsonValue &json, bool indent, bool sort_keys)
{
    return dump_json(stdout, json, indent, sort_keys);
}

std::string load_bytes(const std::string &path)
{
    std::ifstream t(path.c_str());
    std::stringstream buffer;
    buffer << t.rdbuf();
    return buffer.str();
}
std::string load_bytes()
{
    std::istreambuf_iterator<char> begin(std::cin), end;
    return std::string(begin, end);
}
bool dump_bytes(const std::string &path, const std::string &bytes)
{
    std::ofstream outfile(path, std::ofstream::binary | std::ios::out);
    if (!outfile) {
        return false;
    }
    outfile.write(bytes.data(), bytes.size());
    return true;
}

template <typename T> RapidjsonValue to_json(const T &t)
{
    RapidjsonAllocator allocator;
    return T::visit(t, mapbox::geojson::to_value{allocator});
}

RapidjsonValue geojson2json(const mapbox::geojson::value &geojson,
                            bool sort_keys)
{
    auto json = to_json(geojson);
    if (sort_keys) {
        sort_keys_inplace(json);
    }
    return json;
}

RapidjsonValue geojson2json(const mapbox::geojson::geojson &geojson,
                            bool sort_keys)
{
    RapidjsonAllocator allocator;
    auto json = mapbox::geojson::convert(geojson, allocator);
    if (sort_keys) {
        sort_keys_inplace(json);
    }
    return json;
}

mapbox::geojson::value json2geojson(const RapidjsonValue &json)
{
    return mapbox::geojson::convert<mapbox::geojson::value>(json);
}

RapidjsonValue parse(const std::string &json, bool raise_error)
{
    RapidjsonDocument d;
    rapidjson::StringStream ss(json.c_str());
    d.ParseStream<RJFLAGS>(ss);
    if (d.HasParseError()) {
        if (raise_error) {
            throw std::invalid_argument(
                "invalid json, offset: " + std::to_string(d.GetErrorOffset()) +
                ", error: " + rapidjson::GetParseError_En(d.GetParseError()));
        } else {
            return RapidjsonValue{};
        }
    }
    return RapidjsonValue{std::move(d.Move())};
}

std::string dump(const RapidjsonValue &json, bool indent, bool _sort_keys)
{
    if (_sort_keys) {
        auto sorted = sort_keys(json);
        return dump(sorted, indent, false);
    }
    rapidjson::StringBuffer buffer;
    if (indent) {
        rapidjson::PrettyWriter<rapidjson::StringBuffer> writer(buffer);
        json.Accept(writer);
    } else {
        rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
        json.Accept(writer);
    }
    return buffer.GetString();
}

std::string dump(const mapbox::geojson::value &geojson, bool indent,
                 bool sort_keys)
{
    auto json = to_json(geojson);
    if (sort_keys) {
        sort_keys_inplace(json);
    }
    return dump(json, indent);
}

std::string dump(const mapbox::geojson::geojson &geojson, //
                 bool indent,                             //
                 bool sort_keys)
{
    RapidjsonAllocator allocator;
    auto json = mapbox::geojson::convert(geojson, allocator);
    if (sort_keys) {
        sort_keys_inplace(json);
    }
    return dump(json, indent);
}

std::string Encoder::encode(const mapbox::geojson::geojson &geojson)
{
    dim = MAPBOX_GEOBUF_DEFAULT_DIM;
    e = 1;
    keys.clear();
    analyze(geojson);
    if (onlyXY) {
        dim = dimXY;
    }
    std::string data;
    Encoder::Pbf pbf{data};
    {
        auto kk = std::set<std::string>();
        for (auto &pair : keys) {
            kk.insert(pair.first);
        }
        int idx = -1;
        for (auto &k : kk) {
            pbf.add_string(1, k);
            keys[k] = ++idx;
        }
    }
    if (dim != MAPBOX_GEOBUF_DEFAULT_DIM) {
        pbf.add_uint32(2, dim);
    }
    const uint32_t precision = std::log10(std::min(e, maxPrecision));
    if (precision !=
        MAPBOX_GEOBUF_DEFAULT_PRECISION) { // assumed default precision in proto
        pbf.add_uint32(3, precision);
    }
    geojson.match(
        [&](const mapbox::geojson::feature_collection &features) {
            protozero::pbf_writer pbf_fc{pbf, 4};
            writeFeatureCollection(features, pbf_fc);
        },
        [&](const mapbox::geojson::feature &feature) {
            protozero::pbf_writer pbf_f{pbf, 5};
            writeFeature(feature, pbf_f);
        },
        [&](const mapbox::geojson::geometry &geometry) {
            protozero::pbf_writer pbf_g{pbf, 6};
            writeGeometry(geometry, pbf_g);
        });
    return data;
}

std::string Encoder::encode(const mapbox::geojson::feature_collection &features)
{
    dim = MAPBOX_GEOBUF_DEFAULT_DIM;
    e = 1;
    keys.clear();
    analyze(features);
    if (onlyXY) {
        dim = dimXY;
    }
    std::string data;
    Encoder::Pbf pbf{data};
    {
        auto kk = std::set<std::string>();
        for (auto &pair : keys) {
            kk.insert(pair.first);
        }
        int idx = -1;
        for (auto &k : kk) {
            pbf.add_string(1, k);
            keys[k] = ++idx;
        }
    }
    if (dim != MAPBOX_GEOBUF_DEFAULT_DIM) {
        pbf.add_uint32(2, dim);
    }
    const uint32_t precision = std::log10(std::min(e, maxPrecision));
    if (precision !=
        MAPBOX_GEOBUF_DEFAULT_PRECISION) { // assumed default precision in proto
        pbf.add_uint32(3, precision);
    }
    protozero::pbf_writer pbf_fc{pbf, 4};
    writeFeatureCollection(features, pbf_fc);
    return data;
}

std::string Encoder::encode(const std::string &geojson_text)
{
    if (geojson_text.empty()) {
        return "";
    }
    if (geojson_text[0] != '{') {
        auto json = mapbox::geobuf::load_json(geojson_text);
        return encode(mapbox::geojson::convert(json));
    }
    auto geojson = mapbox::geojson::convert(parse(geojson_text));
    return encode(geojson);
}

std::string Encoder::encode(const RapidjsonValue &json)
{
    auto geojson = mapbox::geojson::convert(json);
    return encode(geojson);
}

bool Encoder::encode(const std::string &input_path,
                     const std::string &output_path)
{
    auto json = mapbox::geobuf::load_json(input_path);
    auto bytes = encode(mapbox::geojson::convert(json));
    return dump_bytes(output_path, bytes);
}

void Encoder::analyze(const mapbox::geojson::geojson &geojson)
{
    geojson.match(
        [&](const mapbox::geojson::feature &f) { analyzeFeature(f); },
        [&](const mapbox::geojson::geometry &g) { analyzeGeometry(g); },
        [&](const mapbox::geojson::feature_collection &fc) {
            for (auto &f : fc) {
                analyzeFeature(f);
            }
            saveKey(fc.custom_properties);
        });
}

void Encoder::analyze(const mapbox::geojson::feature_collection &features)
{
    for (auto &f : features) {
        analyzeFeature(f);
    }
    saveKey(features.custom_properties);
}

void Encoder::analyzeFeature(const mapbox::geojson::feature &f)
{
    saveKey(f.properties);
    saveKey(f.custom_properties);
    analyzeGeometry(f.geometry);
}

void Encoder::analyzeGeometry(const mapbox::geojson::geometry &geometry)
{
    geometry.match(
        [&](const mapbox::geojson::point &point) { analyzePoint(point); },
        [&](const mapbox::geojson::multi_point &points) {
            analyzePoints(points);
        },
        [&](const mapbox::geojson::line_string &points) {
            analyzePoints(points);
        },
        [&](const mapbox::geojson::polygon &polygon) {
            analyzeMultiLine((LinesType &)polygon);
        },
        [&](const mapbox::geojson::multi_line_string &lines) {
            analyzeMultiLine(lines);
        },
        [&](const mapbox::geojson::multi_polygon &polygons) {
            for (auto &polygon : polygons) {
                analyzeMultiLine((LinesType &)polygon);
            }
        },
        [&](const mapbox::geojson::geometry_collection &geoms) {
            for (auto &geom : geoms) {
                analyzeGeometry(geom);
            }
        },
        [&](const mapbox::geojson::empty &null) {});
    saveKey(geometry.custom_properties);
}

void Encoder::analyzeMultiLine(const LinesType &lines)
{
    for (auto &line : lines) {
        analyzePoints(line);
    }
}
void Encoder::analyzePoints(const PointsType &points)
{
    for (auto &point : points) {
        analyzePoint(point);
    }
}

inline double ROUND(double v, double s)
{
    return std::floor(v * s + 0.5) / s;
    // return std::round(v * s) / s;
}

void Encoder::analyzePoint(const mapbox::geojson::point &point)
{
    if (!onlyXY && dim < dimXYZ) {
        dim = std::max(point.z == 0 ? dimXY : dimXYZ, dim);
    }
    if (e >= maxPrecision) {
        return;
    }
    const double *ptr = &point.x;
    for (int i = 0; i < dim; ++i) {
        while (ROUND(ptr[i], e) != ptr[i] && e < maxPrecision) {
            e *= 10;
        }
    }
}
void Encoder::saveKey(const std::string &key)
{
    keys.try_emplace(key, keys.size());
}

void Encoder::saveKey(const mapbox::feature::property_map &props)
{
    for (auto &pair : props) {
        saveKey(pair.first);
    }
}

inline std::string to_hex(const std::string &s, bool upper_case = true)
{
    std::ostringstream ret;
    ret << s.size() << " bytes\n";

    for (std::string::size_type i = 0; i < s.length(); ++i) {
        if (i % 80 == 0) {
            ret << fmt::format("\n\t#{:4d}: ", i);
        }
        int z = s[i] & 0xff;
        ret << std::hex << std::setfill('0') << std::setw(2)
            << (upper_case ? std::uppercase : std::nouppercase) << z;
    }

    return ret.str();
}

void Encoder::writeFeatureCollection(
    const mapbox::geojson::feature_collection &geojson, Pbf &pbf)
{
    std::vector<std::string> toprint;
    for (auto &feature : geojson) {
        protozero::pbf_writer pbf_f{pbf, 1};
        writeFeature(feature, pbf_f);
    }
    if (!geojson.custom_properties.empty()) {
        writeProps(geojson.custom_properties, pbf, 15);
    }
}

void Encoder::writeFeature(const mapbox::geojson::feature &feature, Pbf &pbf)
{
    if (!feature.geometry.is<mapbox::geojson::empty>()) {
        protozero::pbf_writer pbf_geom{pbf, 1};
        writeGeometry(feature.geometry, pbf_geom);
    }
    if (!feature.id.is<mapbox::geojson::null_value_t>()) {
        // https://github.com/mapbox/geobuf/blob/daad5e039f842f4d4f24ed7d59f31586563b71b8/geobuf.proto#L18-L21
        // oneof id_type {
        //     string id = 11;
        //     sint64 int_id = 12;
        // }
        // using identifier = mapbox::util::variant<null_value_t, uint64_t,
        // int64_t, double, std::string>;
        feature.id.match(
            [&](uint64_t uid) {
                if (uid <= static_cast<uint64_t>(
                               std::numeric_limits<int64_t>::max())) {
                    pbf.add_int64(12, static_cast<int64_t>(uid));
                } else {
                    pbf.add_string(11, std::to_string(uid));
                }
            },
            [&](int64_t id) { pbf.add_int64(12, id); },
            [&](double d) {
                rapidjson::StringBuffer s;
                rapidjson::Writer<rapidjson::StringBuffer> writer(s);
                writer.Double(d);
                pbf.add_string(11, s.GetString());
            },
            [&](const std::string &id) { pbf.add_string(11, id); },
            [&](const auto &) {
                throw std::invalid_argument("invalid id: " +
                                            dump(to_json(feature.id)));
            });
    }
    if (!feature.properties.empty()) {
        writeProps(feature.properties, pbf, 14);
    }
    if (!feature.custom_properties.empty()) {
        writeProps(feature.custom_properties, pbf, 15);
    }
}

void Encoder::writeGeometry(const mapbox::geojson::geometry &geometry,
                            Encoder::Pbf &pbf)
{
    geometry.match(
        [&](const mapbox::geojson::point &point) {
            pbf.add_enum(1, 0);
            writePoint(point, pbf);
        },
        [&](const mapbox::geojson::multi_point &points) {
            pbf.add_enum(1, 1);
            writeLine(points, pbf);
        },
        [&](const mapbox::geojson::line_string &lines) {
            pbf.add_enum(1, 2);
            writeLine(lines, pbf);
        },
        [&](const mapbox::geojson::multi_line_string &lines) {
            pbf.add_enum(1, 3);
            writeMultiLine((LinesType &)lines, pbf, false);
        },
        [&](const mapbox::geojson::polygon &polygon) {
            pbf.add_enum(1, 4);
            writeMultiLine((LinesType &)polygon, pbf, true);
        },
        [&](const mapbox::geojson::multi_polygon &polygons) {
            pbf.add_enum(1, 5);
            writeMultiPolygon(polygons, pbf);
        },
        [&](const mapbox::geojson::geometry_collection &geometries) {
            pbf.add_enum(1, 6);
            for (auto &geom : geometries) {
                protozero::pbf_writer pbf_sub{pbf, 4};
                writeGeometry(geom, pbf_sub);
            }
        },
        [&](const mapbox::geojson::empty &empty) {});
    if (!geometry.custom_properties.empty()) {
        writeProps(geometry.custom_properties, pbf, 15);
    }
}

void Encoder::writeProps(const mapbox::feature::property_map &props,
                         Encoder::Pbf &pbf, int tag)
{
    std::vector<uint32_t> indexes;
    int valueIndex = 0;
    std::vector<std::pair<std::string, const mapbox::feature::value *>> kv;
    kv.reserve(props.size());
    for (auto &pair : props) {
        kv.emplace_back(pair.first, &pair.second);
    }
    std::sort(kv.begin(), kv.end(), [](const auto &p1, const auto &p2) {
        return p1.first < p2.first;
    });
    for (auto &pair : kv) {
        protozero::pbf_writer pbf_value{pbf, 13};
        writeValue(*pair.second, pbf_value);
        indexes.push_back(keys.at(pair.first));
        indexes.push_back(valueIndex++);
    }
    pbf.add_packed_uint32(tag, indexes.begin(), indexes.end());
}

void Encoder::writeValue(const mapbox::feature::value &value, Encoder::Pbf &pbf)
{
    // message Value {
    //     oneof value_type {
    //         string string_value = 1;
    //         double double_value = 2;
    //         uint64 pos_int_value = 3;
    //         uint64 neg_int_value = 4;
    //         bool bool_value = 5;
    //         string json_value = 6;
    //     }
    // }
    value.match([&](bool val) { pbf.add_bool(5, val); },
                [&](uint64_t val) { pbf.add_uint64(3, val); },
                [&](int64_t val) { pbf.add_uint64(4, -val); },
                [&](double val) { pbf.add_double(2, val); },
                [&](const std::string &val) { pbf.add_string(1, val); },
                [&](const auto &) { pbf.add_string(6, dump(to_json(value))); });
    //
}

void Encoder::writePoint(const mapbox::geojson::point &point, Encoder::Pbf &pbf)
{
    std::array<int64_t, 3> coords;
    coords[0] = static_cast<int64_t>(std::floor(point.x * e + 0.5));
    coords[1] = static_cast<int64_t>(std::floor(point.y * e + 0.5));
    if (dim == 3) {
        double z = zScale ? ROUND(point.z, *zScale) : point.z;
        coords[2] = static_cast<int64_t>(std::floor(z * e + 0.5));
    }
    pbf.add_packed_sint64(3, &coords[0], &coords[0] + dim);
}

void Encoder::writeLine(const PointsType &line, Encoder::Pbf &pbf)
{
    auto coords = populateLine(line, false);
    pbf.add_packed_sint64(3, coords.begin(), coords.end());
}
void Encoder::writeMultiLine(const LinesType &lines, Encoder::Pbf &pbf,
                             bool closed)
{
    int len = lines.size();
    if (len != 1) {
        std::vector<std::uint32_t> lengths;
        lengths.reserve(len);
        for (auto &line : lines) {
            lengths.push_back(line.size() - (closed ? 1 : 0));
        }
        pbf.add_packed_uint32(2, lengths.begin(), lengths.end());
    }
    std::vector<int64_t> coords;
    for (auto &line : lines) {
        populateLine(coords, line, closed);
    }
    pbf.add_packed_sint64(3, coords.begin(), coords.end());
}
void Encoder::writeMultiPolygon(const PolygonsType &polygons, Encoder::Pbf &pbf)
{
    int len = polygons.size();
    if (len != 1 || polygons[0].size() != 1) {
        std::vector<std::uint32_t> lengths;
        lengths.push_back(len); // n_polygons
        for (auto &polygon : polygons) {
            lengths.push_back(polygon.size()); // n_rings
            for (auto &ring : polygon) {
                lengths.push_back(ring.size() - 1); // n_points
            }
        }
        pbf.add_packed_uint32(2, lengths.begin(), lengths.end());
    }
    std::vector<int64_t> coords;
    for (auto &polygon : polygons) {
        for (auto &ring : polygon) {
            populateLine(coords, ring, true);
        }
    }
    pbf.add_packed_sint64(3, coords.begin(), coords.end());
}

std::vector<int64_t> Encoder::populateLine(const PointsType &line, bool closed)
{
    std::vector<int64_t> coords;
    populateLine(coords, line, closed);
    return coords;
}

void Encoder::populateLine(std::vector<int64_t> &coords, //
                           const PointsType &line,       //
                           bool closed)
{
    coords.reserve(coords.size() + dim * line.size());
    int len = line.size() - (closed ? 1 : 0);
    auto sum = std::array<int64_t, 3>{0, 0, 0};
    for (int i = 0; i < len; ++i) {
        const auto &pt = line[i];
        auto n = static_cast<int64_t>(std::floor(pt.x * e + 0.5)) - sum[0];
        coords.push_back(n);
        sum[0] += n;
        n = static_cast<int64_t>(std::floor(pt.y * e + 0.5)) - sum[1];
        coords.push_back(n);
        sum[1] += n;
        if (dim == 3) {
            double z = zScale ? ROUND(pt.z, *zScale) : pt.z;
            n = static_cast<int64_t>(std::floor(z * e + 0.5)) - sum[2];
            coords.push_back(n);
            sum[2] += n;
        }
    }
}

std::string Decoder::to_printable(const std::string &pbf_bytes,
                                  const std::string &indent)
{
    // TODO, read the code
    return ::decode(pbf_bytes.data(), pbf_bytes.size(), indent);
}

mapbox::geojson::geojson Decoder::decode(const uint8_t *data, size_t size)
{
    dim = MAPBOX_GEOBUF_DEFAULT_DIM;
    e = std::pow(10, MAPBOX_GEOBUF_DEFAULT_PRECISION);
    keys.clear();
    head = (const char *)data;
    auto pbf = protozero::pbf_reader{head, size};
    while (pbf.next()) {
        const auto tag = pbf.tag();
        if (tag == 1) {
            keys.push_back(pbf.get_string());
            header_size = pbf.data().data() - head;
        } else if (tag == 2) {
            dim = pbf.get_uint32();
            header_size = pbf.data().data() - head;
        } else if (tag == 3) {
            e = std::pow(10, pbf.get_uint32());
            header_size = pbf.data().data() - head;
        } else if (tag == 4) {
            protozero::pbf_reader pbf_fc = pbf.get_message();
            return readFeatureCollection(pbf_fc);
        } else if (tag == 5) {
            protozero::pbf_reader pbf_f = pbf.get_message();
            return readFeature(pbf_f);
        } else if (tag == 6) {
            protozero::pbf_reader pbf_g = pbf.get_message();
            return readGeometry(pbf_g);
        } else {
            pbf.skip();
        }
    }
    return mapbox::geojson::geojson{};
}

void Decoder::decode_header(const uint8_t *data, std::size_t size)
{
    dim = MAPBOX_GEOBUF_DEFAULT_DIM;
    e = std::pow(10, MAPBOX_GEOBUF_DEFAULT_PRECISION);
    keys.clear();
    auto pbf =
        protozero::pbf_reader{reinterpret_cast<const char *>(data), size};
    while (pbf.next()) {
        const auto tag = pbf.tag();
        if (tag == 1) {
            keys.push_back(pbf.get_string());
        } else if (tag == 2) {
            dim = pbf.get_uint32();
        } else if (tag == 3) {
            e = std::pow(10, pbf.get_uint32());
        } else {
            return;
        }
    }
}

std::optional<mapbox::geojson::feature>
Decoder::decode_feature(const uint8_t *data, std::size_t size,
                        bool only_geometry, bool only_properties)
{
    try {
        auto pbf =
            protozero::pbf_reader{reinterpret_cast<const char *>(data), size};
        if (!pbf.next() || pbf.tag() != 1) {
            return {};
        }
        auto pbf_f = pbf.get_message();
        return readFeature(pbf_f, only_geometry, only_properties);
    } catch (...) {
        return {};
    }
}

inline void unpack_properties(mapbox::geojson::prop_map &properties,
                              const std::vector<uint32_t> &indexes,
                              const std::vector<std::string> &keys,
                              const std::vector<mapbox::geojson::value> &values)
{
    for (auto it = indexes.begin(); it != indexes.end();) {
        auto &key = keys[*it++];
        auto &value = values[*it++];
        properties[key] = value;
    }
}

mapbox::feature::value Decoder::decode_non_features(const uint8_t *data,
                                                    std::size_t size)
{
    try {
        auto pbf =
            protozero::pbf_reader{reinterpret_cast<const char *>(data), size};
        std::vector<mapbox::geojson::value> values;
        auto props = mapbox::feature::property_map{};
        while (pbf.next()) {
            const auto tag = pbf.tag();
            if (tag == 13) {
                protozero::pbf_reader pbf_v = pbf.get_message();
                values.push_back(readValue(pbf_v));
            } else if (tag == 15) {
                auto indexes = pbf.get_packed_uint32();
                if (indexes.size() % 2 != 0) {
                    continue;
                }
                unpack_properties(
                    props,                                                 //
                    std::vector<uint32_t>(indexes.begin(), indexes.end()), //
                    keys, values);
                values.clear();
            } else {
                pbf.skip();
            }
        }
        return props;
    } catch (...) {
    }
    return {};
}

mapbox::geojson::geojson Decoder::decode_file(const std::string &geobuf_path)
{
    auto bytes = load_bytes(geobuf_path);
    return decode((const uint8_t *)bytes.data(), bytes.size());
}

bool Decoder::decode(const std::string &input_path,
                     const std::string &output_path, //
                     bool indent, bool sort_keys)
{
    auto bytes = load_bytes(input_path);
    auto geojson = decode((const uint8_t *)bytes.data(), bytes.size());
    auto json = geojson2json(geojson, sort_keys);
    return dump_json(output_path, json, indent);
}

mapbox::geojson::feature_collection Decoder::readFeatureCollection(Pbf &pbf)
{
    mapbox::geojson::feature_collection fc;
    std::vector<mapbox::geojson::value> values;
    offsets.clear();
    std::optional<uint64_t> props_cursor;
    while (true) {
        uint64_t cursor = pbf.data().data() - head;
        if (!pbf.next()) {
            break;
        }
        const auto tag = pbf.tag();
        if (tag == 1) {
            protozero::pbf_reader pbf_f = pbf.get_message();
            fc.push_back(readFeature(pbf_f));
            offsets.push_back(cursor);
            continue;
        }
        if (!props_cursor) {
            props_cursor = cursor;
        }
        if (tag == 13) {
            protozero::pbf_reader pbf_v = pbf.get_message();
            values.push_back(readValue(pbf_v));
        } else if (tag == 15) {
            auto indexes = pbf.get_packed_uint32();
            if (indexes.size() % 2 != 0) {
                continue;
            }
            unpack_properties(
                fc.custom_properties,                                  //
                std::vector<uint32_t>(indexes.begin(), indexes.end()), //
                keys, values);
            values.clear();
        } else {
            pbf.skip();
        }
    }
    // props start
    uint64_t tail = pbf.data().data() - head;
    if (props_cursor && !offsets.empty() && *props_cursor > offsets.back()) {
        offsets.push_back(*props_cursor);
    } else {
        offsets.push_back(tail);
    }
    // final tail
    offsets.push_back(tail);
    return fc;
}

mapbox::geojson::feature Decoder::readFeature(Pbf &pbf)
{
    mapbox::geojson::feature f;
    std::vector<mapbox::geojson::value> values;
    while (pbf.next()) {
        const auto tag = pbf.tag();
        if (tag == 1) {
            protozero::pbf_reader pbf_g = pbf.get_message();
            f.geometry = readGeometry(pbf_g);
        } else if (tag == 11) {
            // see "feature.id.match(" in this source file
            // protobuf:    oneof id_type {
            //                  string id = 11;
            //                  sint64 int_id = 12;
            //              }
            // geojson:     id := <null, uint64_t, int64_t, double, string>
            auto text = pbf.get_string();
            auto json = parse(text);
            if (json.IsNumber()) {
                if (json.IsUint64()) {
                    f.id = json.GetUint64();
                } else if (json.IsInt64()) {
                    f.id = json.GetInt64();
                } else {
                    f.id = json.GetDouble();
                }
            } else {
                f.id = text;
            }
        } else if (tag == 12) {
            f.id = pbf.get_int64();
        } else if (tag == 13) {
            protozero::pbf_reader pbf_v = pbf.get_message();
            values.push_back(readValue(pbf_v));
        } else if (tag == 14) {
            auto indexes = pbf.get_packed_uint32();
            if (indexes.size() % 2 != 0) {
                continue;
            }
            unpack_properties(
                f.properties,                                          //
                std::vector<uint32_t>(indexes.begin(), indexes.end()), //
                keys, values);
            values.clear();
        } else if (tag == 15) {
            auto indexes = pbf.get_packed_uint32();
            if (indexes.size() % 2 != 0) {
                continue;
            }
            unpack_properties(
                f.custom_properties,                                   //
                std::vector<uint32_t>(indexes.begin(), indexes.end()), //
                keys, values);
            values.clear();
        } else {
            pbf.skip();
        }
    }
    return f;
}

mapbox::geojson::feature Decoder::readFeature(Pbf &pbf, //
                                              bool only_geometry,
                                              bool only_properties)
{
    if (!only_geometry && !only_properties) {
        return readFeature(pbf);
    } else if (only_geometry) {
        while (pbf.next(1)) {
            protozero::pbf_reader pbf_g = pbf.get_message();
            return mapbox::geojson::feature{readGeometry(pbf_g)};
        }
        return {};
    } else if (only_properties) {
        mapbox::geojson::feature f;
        std::vector<mapbox::geojson::value> values;
        while (pbf.next()) {
            const auto tag = pbf.tag();
            if (tag == 13) {
                protozero::pbf_reader pbf_v = pbf.get_message();
                values.push_back(readValue(pbf_v));
            } else if (tag == 14) {
                auto indexes = pbf.get_packed_uint32();
                if (indexes.size() % 2 != 0) {
                    continue;
                }
                unpack_properties(
                    f.properties,                                          //
                    std::vector<uint32_t>(indexes.begin(), indexes.end()), //
                    keys, values);
                values.clear();
            } else {
                pbf.skip();
            }
        }
        return f;
    }
    return {};
}

std::vector<mapbox::geojson::point>
populate_points(const std::vector<int64_t> &int64s, //
                int start_index, int length,        //
                int dim, double e, bool closed = false)
{
    auto coords = std::vector<mapbox::geojson::point>{};
    coords.resize(length + (closed ? 1 : 0));
    auto prevP = std::array<int64_t, 3>{0, 0, 0};
    for (int i = 0; i < length; ++i) {
        double *p = &coords[i].x;
        for (int d = 0; d < dim; ++d) {
            prevP[d] += int64s[(start_index + i) * dim + d];
            p[d] = prevP[d] / e;
        }
    }
    if (closed) {
        coords.back() = coords.front();
    }
    return coords;
}

mapbox::geojson::geometry Decoder::readGeometry(Pbf &pbf)
{
    if (!pbf.next()) {
        return {};
    }
    const auto type = pbf.get_enum();
    auto populatePoint = [&](mapbox::geojson::geometry &point,
                             const std::vector<int64_t> &coords) {
        if (dim == 3) {
            point =
                mapbox::geojson::point(coords[0] / static_cast<double>(e), //
                                       coords[1] / static_cast<double>(e), //
                                       coords[2] / static_cast<double>(e));
        } else {
            point =
                mapbox::geojson::point(coords[0] / static_cast<double>(e), //
                                       coords[1] / static_cast<double>(e));
        }
    };

    auto populateMultiPoint = [&](mapbox::geojson::geometry &points,
                                  const std::vector<int64_t> &coords) {
        points = mapbox::geojson::multi_point{
            populate_points(coords,                 //
                            0, coords.size() / dim, //
                            dim, e)};
    };

    auto populateLineString = [&](mapbox::geojson::geometry &line,
                                  const std::vector<int64_t> &coords) {
        line = mapbox::geojson::line_string{
            populate_points(coords,                 //
                            0, coords.size() / dim, //
                            dim, e)};
    };

    auto populateMultiLineString = [&](mapbox::geojson::geometry &lines,
                                       const std::vector<uint32_t> &lengths,
                                       const std::vector<int64_t> &coords) {
        if (lengths.empty()) {
            lines = mapbox::geojson::multi_line_string{
                {populate_points(coords, 0, coords.size() / dim, dim, e)}};
        } else {
            int lastIndex = 0;
            auto ret = mapbox::geojson::multi_line_string{};
            ret.reserve(lengths.size());
            for (auto length : lengths) {
                ret.push_back(mapbox::geojson::line_string{
                    populate_points(coords, lastIndex, length, dim, e)});
                lastIndex += length;
            }
            lines = std::move(ret);
        }
    };

    auto populatePolygon = [&](mapbox::geojson::geometry &polygon,
                               const std::vector<uint32_t> &lengths,
                               const std::vector<int64_t> &coords) {
        if (lengths.empty()) {
            auto shell = mapbox::geojson::line_string{
                populate_points(coords, 0, coords.size() / dim, dim, e, true)};
            polygon = mapbox::geojson::polygon{{std::move(shell)}};
        } else {
            int lastIndex = 0;
            auto ret = mapbox::geojson::polygon{};
            ret.reserve(lengths.size());
            for (auto length : lengths) {
                ret.push_back(mapbox::geojson::line_string{
                    populate_points(coords, lastIndex, length, dim, e, true)});
                lastIndex += length;
            }
            polygon = std::move(ret);
        }
    };

    auto populateMultiPolygon = [&](mapbox::geojson::geometry &polygons,
                                    const std::vector<uint32_t> &lengths,
                                    const std::vector<int64_t> &coords) {
        if (lengths.empty()) {
            auto shell = mapbox::geojson::line_string{
                populate_points(coords, 0, coords.size() / dim, dim, e, true)};
            polygons = mapbox::geojson::multi_polygon{{{std::move(shell)}}};
        } else {
            auto ret = mapbox::geojson::multi_polygon{};
            int n_polygons = lengths[0];
            ret.reserve(lengths[0]);
            int lastIndex = 0;
            // #polygons #ring ring1_size ring2_size ...
            for (int i = 0, j = 1; i < n_polygons; i++) {
                auto poly = mapbox::geojson::polygon{};
                int n_rings = lengths[j++];
                poly.reserve(n_rings);
                for (int k = 0; k < n_rings; ++k) {
                    int n_points = lengths[j++];
                    auto ring = mapbox::geojson::line_string{populate_points(
                        coords, lastIndex, n_points, dim, e, true)};
                    poly.push_back(std::move(ring));
                    lastIndex += n_points;
                }
                ret.push_back(std::move(poly));
            }
            polygons = std::move(ret);
        }
    };

    std::vector<mapbox::geojson::value> values;
    std::vector<uint32_t> lengths;
    mapbox::geojson::geometry g;
    while (pbf.next()) {
        const auto tag = pbf.tag();
        if (tag == 2) {
            auto uint32s = pbf.get_packed_uint32();
            lengths = std::vector<uint32_t>(uint32s.begin(), uint32s.end());
        } else if (tag == 3) {
            auto int64s = pbf.get_packed_sint64();
            auto coords = std::vector<int64_t>(int64s.begin(), int64s.end());
            if (type == 0) {
                populatePoint(g, coords);
            } else if (type == 1) {
                populateMultiPoint(g, coords);
            } else if (type == 2) {
                populateLineString(g, coords);
            } else if (type == 3) {
                populateMultiLineString(g, lengths, coords);
            } else if (type == 4) {
                populatePolygon(g, lengths, coords);
            } else if (type == 5) {
                populateMultiPolygon(g, lengths, coords);
            } else if (type == 6) {
                //
            } else {
                return g;
            }
        } else if (tag == 4) {
            if (!g.is<mapbox::geojson::geometry_collection>()) {
                g = mapbox::geojson::geometry_collection{};
            }
            protozero::pbf_reader pbf_g = pbf.get_message();
            g.get<mapbox::geojson::geometry_collection>().push_back(
                readGeometry(pbf_g));
        } else if (tag == 13) {
            protozero::pbf_reader pbf_v = pbf.get_message();
            values.push_back(readValue(pbf_v));
        } else if (tag == 15) {
            auto indexes = pbf.get_packed_uint32();
            if (indexes.size() % 2 != 0) {
                continue;
            }
            unpack_properties(
                g.custom_properties,                                   //
                std::vector<uint32_t>(indexes.begin(), indexes.end()), //
                keys, values);
            values.clear();
        } else {
            pbf.skip();
        }
    }
    return g;
}
mapbox::geojson::value Decoder::readValue(Pbf &pbf)
{
    if (!pbf.next()) {
        return {};
    }
    const auto tag = pbf.tag();
    if (tag == 1) {
        return pbf.get_string();
    } else if (tag == 2) {
        return pbf.get_double();
    } else if (tag == 3) {
        return pbf.get_uint64();
    } else if (tag == 4) {
        return static_cast<int64_t>(-pbf.get_uint64());
    } else if (tag == 5) {
        return pbf.get_bool();
    } else if (tag == 6) {
        return json2geojson(parse(pbf.get_string()));
    } else {
        pbf.skip();
    }
    return {};
}
} // namespace geobuf
} // namespace mapbox
