from __future__ import annotations

import base64
import contextlib
import json
import os
import pickle
import shutil
import sys
import tempfile
from copy import deepcopy

import numpy as np
import pytest

import pybind11_geobuf
from pybind11_geobuf import (
    Decoder,
    Encoder,
    GeobufIndex,
    Planet,
    geojson,
    normalize_json,
    pbf_decode,
    rapidjson,
    str2geojson2str,
    str2json2str,
)

__pwd = os.path.abspath(os.path.dirname(__file__))


def test_version():
    print(pybind11_geobuf.__version__)


def sample_geojson():
    return {
        "type": "Feature",
        "properties": {
            "string": "string",
            "int": 42,
            "int2": -101,
            "double": 3.141592653,
            "list": ["a", "list", "is", "a", "list"],
            "dict": {"key": 42, "value": 3.14},
        },
        "geometry": {
            "coordinates": [
                [120.40317479950272, 31.416966084052177, 1.111111],
                [120.28451900911591, 31.30578266928819, 2.22],
                [120.35592249359615, 31.21781895672254, 3.3333333333333],
                [120.67093786630113, 31.299502266522722, 4.4],
            ],
            "type": "LineString",
            "extra_key": "extra_value",
        },
        "my_key": "my_value",
    }


def test_geobuf():
    geojson = sample_geojson()
    print("input:")
    print(json.dumps(geojson, indent=4))
    print("str2json2str:")
    print(str2json2str(json.dumps(geojson), indent=True, sort_keys=True))
    print("str2geojson2str:")
    print(str2geojson2str(json.dumps(geojson), indent=True, sort_keys=True))

    # precision: 6(default), 7, 8(recommand), 9
    encoder = Encoder()
    assert encoder.max_precision() == 10**6
    assert not encoder.only_xy()
    assert encoder.round_z() is None

    encoder = Encoder(max_precision=int(10**8))
    assert encoder.max_precision() == 10**8
    encoded = encoder.encode(geojson=json.dumps(geojson))
    print("encoded pbf bytes")
    print(pbf_decode(encoded))

    encoder = Encoder(round_z=3)
    assert encoder.round_z() == 3

    with pytest.raises(Exception) as excinfo:
        Encoder(max_precision=int(10**10))  # uint32_t overflow
    assert "incompatible constructor arguments" in repr(excinfo)

    decoder = Decoder()
    geojson_text = decoder.decode(encoded, indent=True)
    print(geojson_text)


def test_geobuf_roundz():
    f = geojson.Feature().from_rapidjson(sample_geojson())
    llas0 = geojson.Feature().from_geobuf(f.to_geobuf()).to_numpy()

    llas = geojson.Feature().from_geobuf(f.to_geobuf(precision=3)).to_numpy()
    assert np.all(np.round(llas, 3) == llas)

    llas = geojson.Feature().from_geobuf(f.to_geobuf(only_xy=True)).to_numpy()
    assert np.all(llas[:, 2] == np.zeros(len(llas)))

    llas = geojson.Feature().from_geobuf(f.to_geobuf(round_z=3)).to_numpy()
    assert np.all(np.round(llas0[:, :2], 8) == llas[:, :2])
    assert np.all(np.round(llas0[:, 2], 3) == llas[:, 2])


def test_rapidjson_empty():
    assert not bool(rapidjson())
    assert not bool(rapidjson([]))
    assert not bool(rapidjson({}))
    assert not bool(rapidjson(0))
    assert not bool(rapidjson(0.0))
    assert not bool(rapidjson(""))
    assert not bool(rapidjson(False))

    assert bool(rapidjson([4]))
    assert bool(rapidjson({"key": "value"}))
    assert bool(rapidjson(-1))
    assert bool(rapidjson(-1.0))
    assert bool(rapidjson("text"))
    assert bool(rapidjson(True))

    assert not rapidjson([4]).Empty()
    assert not rapidjson({"key": "value"}).Empty()
    assert not rapidjson(-1).Empty()
    assert not rapidjson(-1.0).Empty()
    assert not rapidjson("text").Empty()
    assert not rapidjson(True).Empty()

    assert rapidjson([4, 2]).clear() == rapidjson([])
    assert rapidjson([4, 2]).clear() != rapidjson({})
    assert rapidjson({"key": "value"}).clear() == rapidjson({})

    obj1 = rapidjson({"k1": 1, "k2": 2})
    obj2 = rapidjson({"k2": 2, "k1": 1})
    assert obj1 == obj2
    assert list(obj1.keys()) == ["k1", "k2"]
    assert list(obj2.keys()) == ["k2", "k1"]


def test_rapidjson_arr():
    arr = rapidjson([1, 3, "text", {"key": 3.2}])
    assert arr[2]() == "text"
    arr[2] = 789
    assert arr[2]() == 789
    arr[2] = arr()
    arr[0].set({"key": "value"})
    assert arr.dumps() == '[{"key":"value"},3,[1,3,789,{"key":3.2}],{"key":3.2}]'

    obj = rapidjson({"arr": arr})
    assert (
        obj.dumps() == '{"arr":[{"key":"value"},3,[1,3,789,{"key":3.2}],{"key":3.2}]}'
    )


def test_rapidjson_obj():
    geojson = sample_geojson()

    obj = rapidjson(geojson)
    assert obj["type"]
    assert obj["type"]() == "Feature"
    assert id(obj["type"]) == id(obj["type"])
    with pytest.raises(KeyError) as e:
        obj["missing_key"]
    assert "missing_key" in repr(e)
    assert obj.get("missing_key") is None
    assert obj.keys()
    assert obj.values()

    assert obj.dumps()
    assert obj.dumps(indent=True)

    mem = obj["type"].GetRawString()
    assert bytes(mem).decode("utf-8") == "Feature"

    obj2 = obj.clone()
    obj3 = deepcopy(obj)
    assert obj() == obj2() == obj3()

    pickled = pickle.dumps(obj)
    obj4 = pickle.loads(pickled)
    assert obj() == obj4()

    obj.loads("{}")
    assert obj() == {}

    assert not rapidjson(2**63 - 1).IsLosslessDouble()

    obj.SetNull()
    assert obj.GetType().name == "kNullType"
    assert obj() is None

    # https://github.com/pybind/pybind11_json/blob/b02a2ad597d224c3faee1f05a56d81d4c4453092/include/pybind11_json/pybind11_json.hpp#L110
    assert rapidjson(b"raw bytes")() == base64.b64encode(b"raw bytes").decode("utf-8")
    assert rapidjson(b"raw bytes")() == "cmF3IGJ5dGVz"  # base64 encoded
    obj = rapidjson({"bytes": b"raw bytes"})
    obj["other_bytes"] = b"bytes"
    assert obj.dumps() == '{"bytes":"cmF3IGJ5dGVz","other_bytes":"Ynl0ZXM="}'

    basename = "rapidjson.png"
    path = f"{__pwd}/../data/{basename}"
    with open(path, "rb") as f:
        raw_bytes = f.read()
    assert len(raw_bytes) == 5259
    data = {basename: raw_bytes}

    path = f"{__pwd}/{basename}.json"
    if os.path.isfile(path):
        os.remove(path)
    obj = rapidjson(data)
    obj.dump(path, indent=True)
    assert os.path.isfile(path)

    loaded = rapidjson().load(path)
    png = loaded["rapidjson.png"].GetRawString()
    assert len(base64.b64decode(png)) == 5259


def test_rapidjson_sort_dump():
    obj1 = rapidjson(
        {
            "key1": 42,
            "key2": 3.14,
        }
    )
    assert list(obj1.keys()) == ["key1", "key2"]
    assert obj1.dumps() == '{"key1":42,"key2":3.14}'
    assert list(obj1.sort_keys().keys()) == ["key1", "key2"]
    obj2 = rapidjson(
        {
            "key2": 3.14,
            "key1": 42,
        }
    )
    assert list(obj2.keys()) == ["key2", "key1"]
    assert obj2.dumps() == '{"key2":3.14,"key1":42}'
    assert obj2.dumps(sort_keys=True) == '{"key1":42,"key2":3.14}'
    assert (
        obj1.dumps(sort_keys=True, indent=True)
        == '{\n    "key1": 42,\n    "key2": 3.14\n}'
    )
    assert list(obj2.keys()) == ["key2", "key1"]  # won't modify obj
    assert list(obj2.sort_keys().keys()) == ["key1", "key2"]
    obj = rapidjson([obj1, obj2, {"obj2": obj2, "obj1": obj1}])
    obj[0]["another"] = 5
    assert obj1.dumps() == '{"key1":42,"key2":3.14}'
    assert (
        obj.dumps()
        == '[{"key1":42,"key2":3.14,"another":5},{"key1":42,"key2":3.14},{"obj2":{"key1":42,"key2":3.14},"obj1":{"key1":42,"key2":3.14}}]'
    )
    obj.sort_keys()
    assert (
        obj.dumps()
        == '[{"another":5,"key1":42,"key2":3.14},{"key1":42,"key2":3.14},{"obj1":{"key1":42,"key2":3.14},"obj2":{"key1":42,"key2":3.14}}]'
    )

    obj3 = obj
    assert id(obj3) == id(obj)  # python assign
    obj4 = obj.clone()
    obj5 = rapidjson()
    obj5.set(obj)
    assert id(obj4) != id(obj)
    assert id(obj5) != id(obj)
    assert obj4 == obj5
    assert obj4.dumps() == obj5.dumps()
    obj4.push_back(42)
    assert obj4 != obj5
    obj5.push_back(42)
    assert obj4 == obj5

    obj6 = rapidjson().copy_from(obj5)
    assert id(obj6) != id(obj5)
    assert obj6 == obj5


def test_rapidjson_round():
    arr = rapidjson([1.23456, [3.2, 2.345]])
    assert arr() == [1.23456, [3.2, 2.345]]
    arr.round()
    assert arr() == [1.235, [3.2, 2.345]]
    arr.round(precision=2)
    assert arr() == [1.24, [3.2, 2.35]]

    obj = rapidjson(sample_geojson())
    assert obj() == sample_geojson()
    assert (
        obj.clone().round(precision=1).dumps(sort_keys=True)
        == '{"geometry":{"coordinates":[[120.4,31.4,1.1],[120.3,31.3,2.2],[120.4,31.2,3.3],[120.7,31.3,4.4]],"extra_key":"extra_value","type":"LineString"},"my_key":"my_value","properties":{"dict":{"key":42,"value":3.1},"double":3.1,"int":42,"int2":-101,"list":["a","list","is","a","list"],"string":"string"},"type":"Feature"}'
    )
    assert (
        obj.clone().round(precision=1, skip_keys=["geometry"]).dumps(sort_keys=True)
        == '{"geometry":{"coordinates":[[120.40317479950272,31.416966084052177,1.111111],[120.28451900911591,31.30578266928819,2.22],[120.35592249359615,31.21781895672254,3.3333333333333],[120.67093786630113,31.299502266522722,4.4]],"extra_key":"extra_value","type":"LineString"},"my_key":"my_value","properties":{"dict":{"key":42,"value":3.1},"double":3.1,"int":42,"int2":-101,"list":["a","list","is","a","list"],"string":"string"},"type":"Feature"}'
    )


def test_rapidjson_normalize():
    arr = rapidjson([0.0, 0.1, 0.2])
    assert arr.dumps() == "[0.0,0.1,0.2]"
    assert arr.clone().denoise_double_0().dumps() == "[0,0.1,0.2]"

    ls = geojson.LineString().from_numpy(np.ones((2, 2)))
    expected = '{"type":"LineString","coordinates":[[1.0,1.0,0.0],[1.0,1.0,0.0]]}'
    assert ls.to_rapidjson().dumps() == expected
    expected = '{"type":"LineString","coordinates":[[1,1,0],[1,1,0]]}'
    assert ls.to_rapidjson().denoise_double_0().dumps() == expected
    expected = '{"type":"LineString","coordinates":[[1.0,1.0],[1.0,1.0]]}'
    assert ls.to_rapidjson().strip_geometry_z_0().dumps() == expected
    expected = '{"coordinates":[[1,1],[1,1]],"type":"LineString"}'
    assert ls.to_rapidjson().normalize().dumps() == expected
    expected = '{"type":"LineString","coordinates":[[1,1],[1,1]]}'
    assert ls.to_rapidjson().normalize(sort_keys=False).dumps() == expected

    ls.as_numpy()[0, 2] = 0.1
    expected = '{"type":"LineString","coordinates":[[1,1,0.1],[1,1,0]]}'
    assert ls.to_rapidjson().normalize(sort_keys=False).dumps() == expected

    mls = geojson.MultiLineString().from_numpy(np.ones((2, 2)))
    mls.push_back(geojson.LineString().from_numpy(2 * np.ones((3, 2))))
    expected = (
        '{"coordinates":[[[1,1],[1,1]],[[2,2],[2,2],[2,2]]],"type":"MultiLineString"}'
    )
    assert mls.to_rapidjson().normalize().dumps() == expected
    mls[0][0].z = 0.5
    expected = '{"coordinates":[[[1,1,0.5],[1,1,0]],[[2,2,0],[2,2,0],[2,2,0]]],"type":"MultiLineString"}'
    assert mls.to_rapidjson().normalize().dumps() == expected

    llas = np.array([[1.2345678, 2.3456789, 3.456789]])
    ls = geojson.LineString().from_numpy(llas)
    expected = '{"coordinates":[[1.2345678,2.3456789,3.457]],"type":"LineString"}'
    assert ls.to_rapidjson().normalize().dumps() == expected
    expected = '{"coordinates":[[1.235,2.346,3.5]],"type":"LineString"}'
    assert (
        ls.to_rapidjson().normalize(round_geojson_geometry=[3, 3, 1]).dumps()
        == expected
    )
    expected = rapidjson(llas.round(2).tolist()).dumps()
    assert (
        expected
        in ls.to_rapidjson().normalize(round_geojson_geometry=[2, 2, 2]).dumps()
    )

    expected = '{"coordinates":[[1.2345678,2.3456789,3.456789]],"type":"LineString"}'
    assert ls.to_rapidjson().normalize(round_geojson_geometry=None).dumps() == expected

    llas = np.array([[2.5, -10.5, 1.1]])
    ls = geojson.LineString().from_numpy(llas)
    expected = '{"coordinates":[[2.5,-10.5,1]],"type":"LineString"}'
    assert (
        expected
        in ls.to_rapidjson().normalize(round_geojson_geometry=[1, 1, 0]).dumps()
    )
    expected = '{"coordinates":[[3,-10,1]],"type":"LineString"}'
    assert (
        expected
        in ls.to_rapidjson().normalize(round_geojson_geometry=[0, 0, 0]).dumps()
    )

    for scale in [1.0, -1.0]:
        for _ in range(100):
            llas = np.random.random((100, 3)) * scale
            ls = geojson.LineString().from_numpy(llas)
            coords = ls.to_rapidjson().normalize(round_geojson_geometry=[3, 3, 3])()[
                "coordinates"
            ]
            assert np.all(np.array(coords) == np.round(llas, 3))


def test_geojson_point():
    # as_numpy
    g1 = geojson.Point()
    assert np.all(g1.as_numpy() == [0, 0, 0])
    g2 = geojson.Point(1, 2)
    assert np.all(g2.as_numpy() == [1, 2, 0])
    g3 = geojson.Point(1, 2, 3)
    assert np.all(g3.as_numpy() == [1, 2, 3])
    assert list(g3) == [1, 2, 3]
    for x in g3:
        x += 10  # more like value semantic (python can't provide you double&)
    assert list(g3) == [1, 2, 3]
    g1.as_numpy()[:] = 5
    assert np.all(g1.as_numpy() == [5, 5, 5])
    g2.as_numpy()[::2] = 5
    assert np.all(g2.as_numpy() == [5, 2, 5])
    g3.as_numpy()[1:] *= 2
    assert np.all(g3.as_numpy() == [1, 4, 6])

    # to_numpy
    g3.to_numpy()[1:] *= 2
    assert np.all(g3.as_numpy() == [1, 4, 6])

    # from_numpy
    g3.from_numpy([3, 7, 2])
    assert np.all(g3.as_numpy() == [3, 7, 2])

    assert g3() == [3, 7, 2]

    # from/to_rapidjson
    j = g3.to_rapidjson()()
    assert j == {"type": "Point", "coordinates": [3.0, 7.0, 2.0]}
    # update
    g3[0] = 0.0
    assert g3.to_rapidjson()() != {
        "type": "Point",
        "coordinates": [3.0, 7.0, 2.0],
    }
    # reset
    g3.from_rapidjson(rapidjson(j))
    assert g3.to_rapidjson()() == {
        "type": "Point",
        "coordinates": [3.0, 7.0, 2.0],
    }

    # round
    coords = [123.4567890123456, 45.6789012345, 7.89123456]
    g1 = geojson.Point(*coords)
    assert np.all(coords == g1.as_numpy())
    # 8, 8, 3
    assert np.all(g1.round().as_numpy() == [123.45678901, 45.67890123, 7.891])
    g1.round(lon=5, lat=7, alt=2)
    assert np.all(g1.as_numpy() == [123.45679, 45.6789012, 7.89])

    coords = [0.5, -0.5]
    g1 = geojson.Point(*coords)
    g1.round(lon=0, lat=0, alt=0)
    # https://en.cppreference.com/w/cpp/numeric/math/round
    assert np.all(g1.as_numpy() == [1, 0, 0])
    # just like in JS/Python, Math.round(-0.5) => -0.0

    coords = [123, 456]
    g1 = geojson.Point(*coords)
    g1.round(lon=-1, lat=-1)  # normally you don't do it
    assert np.all(g1.as_numpy() == [120, 460, 0])
    assert not g1.deduplicate_xyz()
    assert g1 != geojson.Point()
    g1.clear()
    assert g1 == geojson.Point()


def test_geojson_point2():
    pt = geojson.Point()
    assert pt() == [0.0, 0.0, 0.0]
    pt = geojson.Point([1, 2])
    assert pt() == [1.0, 2.0, 0.0]
    pt = geojson.Point([1, 2, 3])
    assert pt() == [1.0, 2.0, 3.0]
    pt.from_numpy([4, 5, 6])
    assert pt() == [4.0, 5.0, 6.0]
    pt.from_numpy([7, 8])
    assert pt() == [7.0, 8.0, 0.0]
    assert pt.x == 7.0
    pt.x = 6.0
    assert pt.x == 6.0
    assert pt.y == 8.0 and pt.z == 0.0
    assert pt.x == pt[0] == pt[-3]
    assert pt.y == pt[1] == pt[-2]
    assert pt.z == pt[2] == pt[-1]
    pt[2] += 1.0
    assert pt.z == 1.0
    assert pt.to_rapidjson()() == {
        "type": "Point",
        "coordinates": [6.0, 8.0, 1.0],
    }
    pt.from_rapidjson(
        rapidjson(
            {
                "type": "Point",
                "coordinates": [2.0, 4.0, 1.0],
            }
        )
    )
    assert pt.as_numpy().tolist() == [2, 4, 1]
    pt.from_rapidjson(
        rapidjson({"type": "Point", "coordinates": [3.0, 5.0, 2.0]})
    ).x = 33
    assert pt.as_numpy().tolist() == [33, 5, 2]

    pt.clear()
    assert pt() == [0, 0, 0]
    assert pt.clear() == pt


def test_geojson_multi_point():
    g1 = geojson.MultiPoint()
    assert g1.as_numpy().shape == (0, 3)
    g1 = geojson.MultiPoint([[1, 2, 3], [4, 5, 6]])
    assert g1.as_numpy().shape == (2, 3)
    assert len(g1) == 2
    assert np.all(g1.as_numpy() == [[1, 2, 3], [4, 5, 6]])
    assert g1() == [[1, 2, 3], [4, 5, 6]]

    g2 = geojson.MultiPoint([g1[0], g1[1], g1[0], g1[1]])
    assert g2() == [*g1(), *g1()]
    assert len(g2) == 4
    del g2[1]
    assert len(g2) == 3
    assert g2() == [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    assert g2.resize(2)() == [g1[0](), g1[0]()]
    assert len(g2) == 2

    g3 = geojson.MultiPoint([[1, 2], [3, 4]])
    assert np.all(g3.as_numpy() == [[1, 2, 0], [3, 4, 0]])

    assert g1[0]() == [1, 2, 3]
    assert g1[1]() == [4, 5, 6]
    g1[0] = [7, 8, 9]
    g1[1] = [1, 2]
    assert g1() == [[7, 8, 9], [1, 2, 0]]
    g1[1] = geojson.Point([7, 8, 9])
    g1[0] = geojson.Point([1, 2])
    assert g1() == [[1, 2, 0], [7, 8, 9]]
    for idx, pt in enumerate(g1):
        assert isinstance(pt, geojson.Point)
        if idx == 0:
            assert pt() == [1, 2, 0]
        if idx == 1:
            assert pt() == [7, 8, 9]
    g1.append(geojson.Point())
    assert len(g1) == 3  # append works now
    g1.push_back(geojson.Point())
    assert len(g1) == 4  # push_back works now
    g1.pop_back()
    g1.pop_back()
    assert len(g1) == 2

    j = g1.to_rapidjson()
    gg = geojson.MultiPoint().from_rapidjson(j)
    assert g1 == gg
    assert gg() == [[1, 2, 0], [7, 8, 9]]
    assert j() == gg.to_rapidjson()()
    # rapidjson is comparable
    assert j == gg.to_rapidjson()
    j["another_key"] = "value"
    assert j != gg.to_rapidjson()

    xyz = np.zeros(3)
    for x in g1:  # iterable
        xyz += x.as_numpy()
    assert np.all(xyz == np.sum(g1.as_numpy(), axis=0))
    assert np.all(xyz == g1[0].as_numpy() + g1[-1].as_numpy())

    assert len(g1) == 2
    g1.clear()
    assert len(g1) == 0
    assert g1.clear() == g1

    coords = np.array(sample_geojson()["geometry"]["coordinates"])
    g = geojson.MultiPoint(coords)
    assert np.all(
        g.round().as_numpy()
        == [
            [120.4031748, 31.41696608, 1.111],
            [120.28451901, 31.30578267, 2.22],
            [120.35592249, 31.21781896, 3.333],
            [120.67093787, 31.29950227, 4.4],
        ]
    )

    g = geojson.MultiPoint([[1, 2], [1, 2]])
    assert len(g) == 2
    assert g.deduplicate_xyz()
    assert not g.deduplicate_xyz()
    assert len(g) == 1
    g = geojson.MultiPoint([[1, 2], [3, 4], [1, 2]])
    assert len(g) == 3
    assert not g.deduplicate_xyz()
    assert len(g) == 3

    g = geojson.Geometry(g)
    assert len(g) == 3
    g.push_back(geojson.Point(6, 7))
    assert len(g) == 4
    g.clear()
    assert len(g) == 0


def test_geojson_line_string():
    g1 = geojson.LineString()
    assert g1.as_numpy().shape == (0, 3)
    g1 = geojson.LineString([[1, 2, 3], [4, 5, 6]])
    assert g1.as_numpy().shape == (2, 3)
    assert len(g1) == 2
    assert np.all(g1.as_numpy() == [[1, 2, 3], [4, 5, 6]])
    assert g1() == [[1, 2, 3], [4, 5, 6]]

    j = g1.to_rapidjson()
    j["coordinates"] = [[1, 1, 1], [2, 2, 2]]
    g1.from_rapidjson(j)
    assert g1() == [[1, 1, 1], [2, 2, 2]]
    G = geojson.Geometry(g1)
    assert G.to_rapidjson() == g1.to_rapidjson()
    assert G.type() == "LineString"

    assert isinstance(g1, geojson.LineString)

    xyz = np.zeros(3)
    for x in g1:  # iterable
        xyz += x.as_numpy()
    assert np.all(xyz == np.sum(g1.as_numpy(), axis=0))
    assert np.all(xyz == g1[0].as_numpy() + g1[-1].as_numpy())

    assert len(g1) == 2
    g1.push_back([1, 2, 3])
    assert len(g1) == 3
    g1.push_back([4, 5])
    assert len(g1) == 4
    g1.clear()
    assert len(g1) == 0
    assert g1 == g1.clear()

    g1.append(geojson.Point(1, 2))
    assert len(g1) == 1

    coords = np.array(sample_geojson()["geometry"]["coordinates"])
    g = geojson.LineString(coords)
    assert np.all(
        g.round().as_numpy()
        == [
            [120.4031748, 31.41696608, 1.111],
            [120.28451901, 31.30578267, 2.22],
            [120.35592249, 31.21781896, 3.333],
            [120.67093787, 31.29950227, 4.4],
        ]
    )

    g = geojson.LineString([[1, 2, 3], [1, 2, 3], [4, 5, 6]])
    assert len(g) == 3
    assert g.deduplicate_xyz()
    assert not g.deduplicate_xyz()
    assert len(g) == 2


def test_geojson_multi_line_string():
    g1 = geojson.MultiLineString()
    assert isinstance(g1, geojson.MultiLineString)
    assert isinstance(g1, geojson.LineStringList)
    assert len(g1) == 0

    xyzs = [[1, 2, 3], [4, 5, 6]]
    g1.from_numpy(xyzs)
    assert len(g1) == 1
    assert np.all(g1.to_numpy() == xyzs)

    j = g1.to_rapidjson()
    g1.as_numpy()[:] = 1
    assert g1.as_numpy().sum() == 6
    g1.from_rapidjson(j)
    assert np.all(g1.to_numpy() == xyzs)

    coords = np.array(j["coordinates"]())
    assert coords.ndim == 3
    assert coords.shape == (1, 2, 3)
    assert np.array(g1()).shape == (1, 2, 3)

    assert len(g1) == 1
    g10 = g1[0]
    assert isinstance(g10, geojson.LineString)
    for ls in g1:
        assert isinstance(ls, geojson.LineString)
        assert g10 == ls
        assert len(ls) == 2
        for pt in ls:
            assert isinstance(pt, geojson.Point)
            assert len(pt) == 3

    g1.push_back([[1, 2], [3, 4]])
    assert len(g1) == 2
    assert g1() == [
        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
        [[1.0, 2.0, 0.0], [3.0, 4.0, 0.0]],
    ]
    with pytest.raises(ValueError) as excinfo:
        g1.push_back([5, 6])
    assert "shape expected to be Nx2 or Nx3" in repr(excinfo)
    g1[-1].push_back([5, 6])
    assert g1() == [
        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
        [[1.0, 2.0, 0.0], [3.0, 4.0, 0.0], [5.0, 6.0, 0.0]],
    ]
    assert g1() == [g1[0](), g1[1]()]
    g1.from_numpy([[1, 2, 3], [4, 5, 6]])
    assert g1() == [[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]]

    g1[0] = [[7, 8], [2, 3]]
    assert g1() == [[[7, 8, 0], [2, 3, 0]]]

    gg = geojson.Geometry(g1)
    g1.push_back(geojson.LineString([[2, 4, 6], [7, 8, 9]]))
    assert g1() == [[[7, 8, 0], [2, 3, 0]], [[2, 4, 6], [7, 8, 9]]]
    gg.push_back(geojson.LineString([[2, 4, 6], [7, 8, 9]]))
    assert gg()["coordinates"] == [
        [[7, 8, 0], [2, 3, 0]],
        [[2, 4, 6], [7, 8, 9]],
    ]

    g1.clear()
    assert len(g1) == 0

    coords = np.array(sample_geojson()["geometry"]["coordinates"])
    g = geojson.MultiLineString(coords)
    assert np.array(g()).shape == (1, 4, 3)
    assert np.all(
        g.round().as_numpy()
        == [
            [
                [120.4031748, 31.41696608, 1.111],
                [120.28451901, 31.30578267, 2.22],
                [120.35592249, 31.21781896, 3.333],
                [120.67093787, 31.29950227, 4.4],
            ]
        ]
    )
    g.push_back(coords)
    assert np.array(g()).shape == (2, 4, 3)
    assert np.all(
        np.array(g())
        == [
            [
                [120.4031748, 31.41696608, 1.111],
                [120.28451901, 31.30578267, 2.22],
                [120.35592249, 31.21781896, 3.333],
                [120.67093787, 31.29950227, 4.4],
            ],
            coords,
        ]
    )
    assert np.all(
        np.array(g.round()())
        == [
            [
                [120.4031748, 31.41696608, 1.111],
                [120.28451901, 31.30578267, 2.22],
                [120.35592249, 31.21781896, 3.333],
                [120.67093787, 31.29950227, 4.4],
            ],
            [
                [120.4031748, 31.41696608, 1.111],
                [120.28451901, 31.30578267, 2.22],
                [120.35592249, 31.21781896, 3.333],
                [120.67093787, 31.29950227, 4.4],
            ],
        ]
    )

    g = geojson.MultiLineString([[1, 2, 3], [1, 2, 3], [4, 5, 6]])
    assert g.deduplicate_xyz()
    assert not g.deduplicate_xyz()
    g.push_back([[1, 2, 3], [1, 2, 3], [4, 5, 6]])
    assert g.deduplicate_xyz()
    assert not g.deduplicate_xyz()
    g.push_back(g[0])
    assert not g.deduplicate_xyz()


def test_geojson_polygon():
    g1 = geojson.Polygon()
    assert isinstance(g1, geojson.Polygon)
    assert isinstance(g1, geojson.LinearRingList)
    assert len(g1) == 0
    assert g1.to_rapidjson()() == {"type": "Polygon", "coordinates": []}

    g1.from_numpy([[1, 0], [1, 1], [0, 1], [1, 0]])
    assert len(g1) == 1
    assert np.all(
        g1.to_numpy()
        == [
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [1, 0, 0],
        ]
    )
    assert isinstance(g1[0], geojson.LinearRing)
    assert g1[0]() == [
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0],
    ]
    assert g1[0].as_numpy().shape == (4, 3)
    assert len(g1[0]) == 4
    assert len(g1[0][0]) == 3
    for pt in g1[0]:
        assert isinstance(pt, geojson.Point)
    assert isinstance(g1[0][0], geojson.Point)
    for gg in g1:
        assert isinstance(gg, geojson.LinearRing)
        for pt in gg:
            assert isinstance(pt, geojson.Point)

    g1[0].push_back([8, 9]).push_back(geojson.Point(10, 11))
    assert np.all(g1[0].as_numpy()[-2:, :] == [[8, 9, 0], [10, 11, 0]])

    g1[0].from_numpy([[1, 2], [3, 4]])
    assert g1[0]() == [[1.0, 2.0, 0.0], [3.0, 4.0, 0.0]]

    g1.clear()
    assert len(g1) == 0
    assert g1.clear() == g1

    coords = np.array(sample_geojson()["geometry"]["coordinates"])
    g = geojson.Polygon(coords)
    assert np.array(g()).shape == (1, 4, 3)
    assert np.all(
        g.round().as_numpy()
        == [
            [
                [120.4031748, 31.41696608, 1.111],
                [120.28451901, 31.30578267, 2.22],
                [120.35592249, 31.21781896, 3.333],
                [120.67093787, 31.29950227, 4.4],
            ]
        ]
    )
    g.push_back(coords)
    assert np.array(g()).shape == (2, 4, 3)
    assert np.all(
        np.array(g())
        == [
            [
                [120.4031748, 31.41696608, 1.111],
                [120.28451901, 31.30578267, 2.22],
                [120.35592249, 31.21781896, 3.333],
                [120.67093787, 31.29950227, 4.4],
            ],
            coords,
        ]
    )
    assert np.all(
        np.array(g.round()())
        == [
            [
                [120.4031748, 31.41696608, 1.111],
                [120.28451901, 31.30578267, 2.22],
                [120.35592249, 31.21781896, 3.333],
                [120.67093787, 31.29950227, 4.4],
            ],
            [
                [120.4031748, 31.41696608, 1.111],
                [120.28451901, 31.30578267, 2.22],
                [120.35592249, 31.21781896, 3.333],
                [120.67093787, 31.29950227, 4.4],
            ],
        ]
    )

    assert not g.deduplicate_xyz()
    g.round(lon=0, lat=0, alt=-1)
    assert g.deduplicate_xyz()


def test_geojson_multi_polygon():
    g1 = geojson.MultiPolygon()
    assert isinstance(g1, geojson.MultiPolygon)
    assert len(g1) == 0
    assert np.array(g1()).shape == (0,)
    assert g1() == []
    assert g1.to_rapidjson()() == {"type": "MultiPolygon", "coordinates": []}
    g1.from_numpy([[1, 0], [1, 1], [0, 1], [1, 0]])
    assert np.array(g1()).shape == (1, 1, 4, 3)

    assert g1.to_rapidjson()() == {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [1.0, 0.0, 0.0],
                    [1.0, 1.0, 0.0],
                    [0.0, 1.0, 0.0],
                    [1.0, 0.0, 0.0],
                ]
            ]
        ],
    }
    coords = np.array(g1.to_rapidjson()["coordinates"]())
    assert coords.shape == (1, 1, 4, 3)

    g2 = geojson.MultiPolygon().from_rapidjson(g1.to_rapidjson())
    assert g1 == g2

    value = 0
    for polygon in g1:
        assert isinstance(polygon, geojson.Polygon)
        for ring in polygon:
            assert isinstance(ring, geojson.LinearRing)
            for pt in ring:
                assert isinstance(pt, geojson.Point)
                for x in pt:
                    assert isinstance(x, float)
                    value += x
    assert value == 5.0
    assert len(g1) == 1

    assert g1() == [g1[0]()]
    g1[0] = geojson.Polygon([[7, 6, 5]])
    assert g1() == [[[[7.0, 6.0, 5.0]]]]
    g1[0] = [[1, 2, 3]]
    assert g1() == [[[[1.0, 2.0, 3.0]]]]
    g1[0] = [[1, 2]]
    assert g1() == [[[[1.0, 2.0, 0.0]]]]

    with pytest.raises(ValueError) as excinfo:
        g1[0] = [3, 4]  # should be Nx2 or Nx3 (dim==2)
    assert "matrix shape expected to be Nx2 or Nx3, actual=2x1" in repr(excinfo)
    assert g1() == [[[[1.0, 2.0, 0.0]]]]
    with pytest.raises(ValueError) as excinfo:
        g1.push_back([3, 4])
    assert "matrix shape expected to be Nx2 or Nx3, actual=2x1" in repr(excinfo)
    assert g1() == [[[[1.0, 2.0, 0.0]]]]

    g1.push_back([[3, 4]])
    assert g1() == [
        [[[1.0, 2.0, 0.0]]],
        [[[3.0, 4.0, 0.0]]],
    ]

    g1.push_back(geojson.Polygon([[5, 6, 7]]))
    assert g1() == [
        [[[1.0, 2.0, 0.0]]],
        [[[3.0, 4.0, 0.0]]],
        [[[5.0, 6.0, 7.0]]],
    ]
    g1[-1].push_back([[1, 2, 3]]).push_back([[4, 5, 6]])
    assert g1() == [
        [[[1.0, 2.0, 0.0]]],
        [[[3.0, 4.0, 0.0]]],
        [
            [[5.0, 6.0, 7.0]],
            [[1.0, 2.0, 3.0]],
            [[4.0, 5.0, 6.0]],
        ],
    ]
    g1[-1][-1].push_back([7, 8]).push_back([9, 10, 11, 12])
    assert g1() == [
        [[[1.0, 2.0, 0.0]]],
        [[[3.0, 4.0, 0.0]]],
        [
            [[5.0, 6.0, 7.0]],
            [[1.0, 2.0, 3.0]],
            [
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 0.0],
                [9.0, 10.0, 11.0],
            ],
        ],
    ]

    g1.clear()
    assert len(g1) == 0


def test_geojson_geometry_collection():
    gc = geojson.GeometryCollection()
    assert gc() == {"type": "GeometryCollection", "geometries": []}
    assert gc.to_rapidjson()() == {
        "type": "GeometryCollection",
        "geometries": [],
    }
    assert len(gc) == 0

    with pytest.raises(TypeError) as excinfo:
        gc.append(geojson.Point(1, 2))  # won't work
    assert "geojson.Geometry" in repr(excinfo)
    # you can use push_back, it has more overrides
    gc2 = geojson.GeometryCollection()
    gc2.push_back(geojson.Point(1, 2))
    assert gc2() == {
        "type": "GeometryCollection",
        "geometries": [{"type": "Point", "coordinates": [1.0, 2.0, 0.0]}],
    }
    gc2.push_back(geojson.Point(1, 2)).push_back(geojson.MultiPoint()).push_back(
        geojson.LineString()
    )
    gc2.push_back(geojson.MultiLineString()).push_back(geojson.Polygon()).push_back(
        geojson.MultiPolygon()
    )
    gc2.push_back(geojson.GeometryCollection())  # nesting
    # value semantic, push back a current copy, weird but working
    gc2.push_back(geojson.GeometryCollection(gc2))
    # or append Geometry (vector::value_type)
    gc.append(geojson.Geometry(geojson.Point(1, 2)))  # okay
    gc.append(geojson.Geometry(geojson.MultiPoint([[3, 4], [5, 6]])))
    gc.append(geojson.Geometry(geojson.LineString([[7, 8], [9, 10]])))
    assert gc() == {
        "type": "GeometryCollection",
        "geometries": [
            {
                "type": "Point",
                "coordinates": [1.0, 2.0, 0.0],
            },
            {
                "type": "MultiPoint",
                "coordinates": [
                    [3.0, 4.0, 0.0],
                    [5.0, 6.0, 0.0],
                ],
            },
            {
                "type": "LineString",
                "coordinates": [
                    [7.0, 8.0, 0.0],
                    [9.0, 10.0, 0.0],
                ],
            },
        ],
    }
    assert len(gc) == 3
    assert isinstance(gc[0], geojson.Geometry)
    assert gc[2] == gc[-1]

    del gc[0]
    assert len(gc) == 2

    gc[0] = geojson.Geometry(geojson.Point())  # works
    gc[0] = geojson.Point()  # also works
    gc[0] = geojson.MultiPoint()
    gc[0] = geojson.LineString()
    gc[0] = geojson.MultiLineString()
    gc[0] = geojson.Polygon()
    gc[0] = geojson.MultiPolygon()

    gc_init = deepcopy(gc)
    assert gc_init == gc
    del gc[-1]
    assert gc_init != gc
    gc.append(gc_init[-1])
    assert gc_init == gc

    for g in gc:
        isinstance(g, geojson.Geometry)

    gc3 = geojson.GeometryCollection(3)
    assert len(gc3) == 3
    assert gc3() == {
        "type": "GeometryCollection",
        "geometries": [
            None,
            None,
            None,
        ],
    }
    gc3[0] = geojson.Point(1, 2)
    gc3[1] = geojson.Point(3, 4)
    gc3[2] = geojson.Point(5, 6)
    gc3.resize(2)
    assert gc3() == {
        "type": "GeometryCollection",
        "geometries": [
            {"type": "Point", "coordinates": [1.0, 2.0, 0.0]},
            {"type": "Point", "coordinates": [3.0, 4.0, 0.0]},
        ],
    }
    gc3.resize(4)
    assert gc3() == {
        "type": "GeometryCollection",
        "geometries": [
            {"type": "Point", "coordinates": [1.0, 2.0, 0.0]},
            {"type": "Point", "coordinates": [3.0, 4.0, 0.0]},
            None,
            None,
        ],
    }


def test_geojson_geometry():
    g1 = geojson.Geometry()
    assert g1() is None
    assert g1.is_empty()
    assert g1.type() == "None"
    assert g1.as_numpy().shape == (0, 3)

    g2 = geojson.Geometry(geojson.Point())
    assert g2.type() == "Point"
    assert not g2.is_empty()
    assert g2.is_point()
    assert g2() == {"type": "Point", "coordinates": [0.0, 0.0, 0.0]}
    assert len(g2.custom_properties()) == 0
    g2["my_key"] = "my_value"
    assert len(g2.custom_properties()) == 1
    assert g2()["my_key"] == "my_value"
    with pytest.raises(IndexError):  # why not KeyError?
        g2["missing_key"]
    g2.get("missing_key")  # okay to be none
    assert g2() == {
        "type": "Point",
        "coordinates": [0.0, 0.0, 0.0],
        "my_key": "my_value",
    }

    g2["key"] = "wrapped in custom_properties"
    with pytest.raises(KeyError):
        g2["type"] = "type,geometry,properties are reserved"
    assert len(g2) == 3  # size of x,y,z
    assert len(g2.custom_properties()) == 2
    for k in g2:
        assert k in ["key", "my_key"]
    for v in g2.values():
        assert isinstance(v, geojson.value)
    for k, v in g2.items():
        assert k in ["key", "my_key"]
        assert isinstance(v, geojson.value)
    for x in g2.as_point():
        assert x == 0.0

    assert (
        g2.to_rapidjson().sort_keys().dumps()
        == '{"coordinates":[0.0,0.0,0.0],"key":"wrapped in custom_properties","my_key":"my_value","type":"Point"}'
    )
    g2.custom_properties().clear()
    assert len(g2.custom_properties()) == 0
    g2.custom_properties()["key"] = "value"
    assert len(g2.custom_properties()) == 1
    assert geojson.Geometry(g2()) == geojson.Geometry(g2.to_rapidjson()) == g2

    g3 = geojson.Geometry(geojson.MultiPoint([[1, 2, 3]]))
    assert len(g3) == 1  # size of point
    g3.push_back([4, 5])
    g3.push_back(geojson.Point(6, 7))
    assert np.all(g3.as_numpy() == [[1, 2, 3], [4, 5, 0], [6, 7, 0]])
    assert len(g3) == 3
    for pt in g3.as_multi_point():
        assert isinstance(pt, geojson.Point)
        for x in pt:
            assert isinstance(x, float) and 0 <= x <= 7
    assert geojson.Geometry(g3()) == geojson.Geometry(g3.to_rapidjson()) == g3

    g4 = geojson.Geometry(geojson.LineString([[1, 2, 3], [4, 5, 6]]))
    assert g4() == {
        "type": "LineString",
        "coordinates": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
    }
    g4.push_back([7, 8])
    expected = {
        "type": "LineString",
        "coordinates": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 0.0]],
    }
    assert g4() == expected
    g4.push_back(
        [[1, 2, 3], [4, 5, 6]]
    )  # not for LineString, you can only push Nx3 to MultiLineString, Polygon
    expected = {
        "type": "LineString",
        "coordinates": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 0.0]],
    }
    assert g4() == expected
    assert geojson.Geometry(g4()) == geojson.Geometry(g4.to_rapidjson()) == g4

    g5 = geojson.Geometry(geojson.MultiLineString([[1, 2, 3], [4, 5, 6]]))
    g5.push_back([[10, 20, 30], [40, 50, 60]])
    assert g5() == {
        "type": "MultiLineString",
        "coordinates": [
            [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
            [[10.0, 20.0, 30.0], [40.0, 50.0, 60.0]],
        ],
    }
    g5.push_back([70, 80, 90, 100])  # only x, y, z, push to last LineString
    assert g5() == {
        "type": "MultiLineString",
        "coordinates": [
            [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
            [[10.0, 20.0, 30.0], [40.0, 50.0, 60.0], [70.0, 80.0, 90.0]],
        ],
    }
    assert geojson.Geometry(g5()) == geojson.Geometry(g5.to_rapidjson()) == g5
    assert g5() == g5.push_back(g4)()  # push_back geometry silent ignore

    g5 = geojson.Geometry(geojson.MultiLineString())
    with pytest.raises(ValueError) as excinfo:
        g5.push_back([70, 80, 90])
    assert "can't push_back Point to empty MultiLineString" in str(excinfo)
    g5.resize(1)
    assert g5() == {"type": "MultiLineString", "coordinates": [[]]}
    g5.push_back([70, 80, 90])
    assert g5() == {
        "type": "MultiLineString",
        "coordinates": [[[70.0, 80.0, 90.0]]],
    }

    g6 = geojson.Geometry(geojson.Polygon([[1, 2, 3], [4, 5, 6]]))
    assert np.array(g6()["coordinates"]).shape == (1, 2, 3)
    g6.push_back(np.ones((4, 3)))
    assert g6()["coordinates"] == [
        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
        [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
    ]
    g6.push_back([2, 2])
    assert g6()["coordinates"] == [
        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
        [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [2.0, 2.0, 0.0],
        ],
    ]
    assert geojson.Geometry(g6()) == geojson.Geometry(g6.to_rapidjson()) == g6
    g6.clear()
    assert len(g6) == 0
    assert g6.as_numpy().shape == (0, 3)

    g7 = geojson.Geometry(geojson.MultiPolygon([[1, 2, 3], [4, 5, 6]]))
    assert np.array(g7()["coordinates"]).shape == (1, 1, 2, 3)
    assert geojson.Geometry(g7()) == geojson.Geometry(g7.to_rapidjson()) == g7
    assert len(g7) == 1
    g7.as_multi_polygon().push_back(geojson.Polygon([[1, 2, 3], [4, 5, 6]]))
    assert len(g7) == 2
    g7.push_back(geojson.Polygon([[1, 2, 3], [4, 5, 6]]))
    assert len(g7) == 3
    g7.push_back(geojson.Geometry(geojson.Polygon([[1, 2, 3], [4, 5, 6]])))
    assert len(g7) == 4

    gc = geojson.Geometry(geojson.GeometryCollection())
    assert gc.type() == "GeometryCollection"
    gc.push_back(g3)
    assert gc() != gc.push_back(g4)()  # push_back geometry okay
    assert gc() == {"type": gc.type(), "geometries": [g3(), g4()]}
    assert len(gc) == 2

    # update value
    g31 = g3.clone()
    g32 = g3.clone()
    assert g32 == g31
    g31.as_multi_point()[0][0] = 5
    assert g31.as_multi_point()[0][0] == 5
    assert g32 != g31

    gc2 = gc.clone()
    assert gc2() == gc()
    assert id(gc2) != id(gc)

    pickled = pickle.dumps(gc2)
    gc3 = pickle.loads(pickled)
    assert gc3() == gc()
    assert id(gc3) != id(gc)

    gc4 = deepcopy(gc3)
    assert gc4() == gc()
    assert id(gc4) != id(gc)

    assert gc4.__geo_interface__ == gc()

    coords = np.array(sample_geojson()["geometry"]["coordinates"])
    g1 = geojson.Point(coords[0])
    g2 = geojson.MultiPoint(coords)
    g3 = geojson.LineString(coords)
    g4 = geojson.MultiLineString(coords).push_back(coords)
    g5 = geojson.Polygon(coords).push_back(coords)
    g6 = geojson.MultiPolygon(coords).push_back(coords)
    gc = (
        geojson.GeometryCollection()
        .push_back(g1)
        .push_back(g2)
        .push_back(g3)
        .push_back(g4)
        .push_back(g5)
        .push_back(g6)
    )
    assert len(gc) == 6
    assert gc()["type"] == "GeometryCollection"

    gg = geojson.Geometry(gc)
    assert gg() == gc()
    gc.round()
    assert gg() != gc()
    gg.round()
    assert gg() == gc()

    def check_round3(v, n):
        if isinstance(v, float):
            assert v == round(v, n)
        elif isinstance(v, list):
            for e in v:
                check_round3(e, n)
        elif isinstance(v, dict):
            for e in v.values():
                check_round3(e, n)

    check_round3(gc.round(lon=5, lat=5, alt=5)(), 5)
    check_round3(gc.round(lon=3, lat=3, alt=3)(), 3)


def test_geobuf_from_geojson():
    encoder = Encoder(max_precision=int(10**8))
    feature = sample_geojson()
    encoded_0 = encoder.encode(json.dumps(feature))
    print(encoder.keys())
    encoded = encoder.encode(feature)
    assert encoded == encoded_0
    decoder = Decoder()
    decoded = decoder.decode(encoded)
    assert decoder.dim() == 3

    decoded_again = Decoder().decode(Encoder(max_precision=int(10**8)).encode(decoded))
    assert rapidjson().loads(decoded_again) == rapidjson().loads(decoded)
    assert rapidjson().loads(decoded_again) == rapidjson().loads(
        Decoder().decode(encoded)
    )

    j = Decoder().decode_to_rapidjson(encoded)
    g = Decoder().decode_to_geojson(encoded)
    assert g.is_feature()
    f = g.as_feature()
    assert isinstance(f, geojson.Feature)
    with pytest.raises(RuntimeError) as excinfo:
        g.as_geometry()
    assert "in get<T>()" in str(excinfo)
    assert str2json2str(json.dumps(f()), sort_keys=True) == str2json2str(
        decoded, sort_keys=True
    )
    assert str2geojson2str(json.dumps(f()), sort_keys=True) == str2geojson2str(
        decoded, sort_keys=True
    )

    coords = np.array(
        [
            [120.40317479950272, 31.416966084052177, 1.111111],
            [120.28451900911591, 31.30578266928819, 2.22],
            [120.35592249359615, 31.21781895672254, 3.3333333333333],
            [120.67093786630113, 31.299502266522722, 4.4],
        ]
    )
    np.testing.assert_allclose(coords, f.to_numpy(), atol=1e-9)
    np.testing.assert_allclose(coords, f.as_numpy(), atol=1e-9)
    f.to_numpy()[0, 2] = 0.0
    assert f.as_numpy()[0, 2] != 0.0
    f.as_numpy()[0, 2] = 0.0
    assert f.as_numpy()[0, 2] == 0.0

    print(j(), j.dumps())

    expected = str2json2str(json.dumps(feature), indent=True, sort_keys=True)
    actually = str2json2str(decoded, indent=True, sort_keys=True)
    assert len(expected) > 0
    assert len(actually) > 0
    # assert expected == actually # TODO

    encoded1 = encoder.encode(rapidjson(feature))
    assert len(encoded1) == len(encoded)

    decoder = Decoder()
    decoder.decode(
        Encoder(
            max_precision=int(10**8),
            only_xy=True,
        ).encode(json.dumps(feature))
    )
    assert decoder.dim() == 2


def test_geojson_value():
    assert geojson.value().to_rapidjson().dumps() == "null"
    assert geojson.value([]).to_rapidjson().dumps() == "[]"
    assert geojson.value({}).to_rapidjson().dumps() == "{}"
    assert geojson.value("text").to_rapidjson().dumps() == '"text"'
    assert geojson.value(3.14).to_rapidjson().dumps() == "3.14"
    assert geojson.value(42).to_rapidjson().dumps() == "42"


def test_geojson_feature_id():
    feature = geojson.Feature(sample_geojson())
    assert feature.id() is None
    assert feature.id(5).id() == 5
    assert feature.id(None).id() is None
    for fid in [42, -42, 3.14, "id can be string or number"]:
        feature = geojson.Feature({**sample_geojson(), "id": fid})
        assert feature.id() == fid

    # invalid id in json
    with pytest.raises(RuntimeError) as excinfo:
        geojson.Feature({**sample_geojson(), "id": None})
    assert "Feature id must be a string or number" in repr(excinfo)


def test_geojson_feature():
    feature = sample_geojson()
    feature = geojson.Feature(feature)
    assert feature.as_numpy().shape == (4, 3)
    geom = feature.geometry()
    assert geom.type()
    orig = geom.to_numpy()
    llas = geom.as_numpy()
    feature.as_numpy()[:] = 1.0
    assert np.all(llas == 1.0)
    geom.from_numpy(orig)

    props = feature.properties()
    assert not isinstance(props, dict)
    assert isinstance(props, geojson.value.object_type)
    assert (
        props.to_rapidjson().sort_keys().dumps()
        == '{"dict":{"key":42,"value":3.14},"double":3.141592653,"int":42,"int2":-101,"list":["a","list","is","a","list"],"string":"string"}'
    )

    assert set(props.keys()) == {
        "dict",
        "double",
        "int",
        "int2",
        "list",
        "string",
    }
    keys = list(props.keys())
    values = list(props.values())
    for i, (k, v) in enumerate(props.items()):
        assert keys[i] == k
        assert values[i] == v
        assert isinstance(v, geojson.value)

    assert props["list"].is_array()
    for x in list(props["list"].as_array()):
        assert isinstance(x, geojson.value)
        assert type(x) is geojson.value
    with pytest.raises(RuntimeError) as excinfo:
        props["list"].as_object()
    assert "in get<T>()" in repr(excinfo)
    assert len(props["list"]) == 5
    assert props["list"]() == ["a", "list", "is", "a", "list"]
    assert props["list"].as_array()() == ["a", "list", "is", "a", "list"]

    assert props["dict"].is_object()
    for k, v in props["dict"].as_object().items():
        assert isinstance(k, str)
        assert isinstance(v, geojson.value)
        assert type(x) is geojson.value
    with pytest.raises(RuntimeError) as excinfo:
        props["dict"].as_array()
    assert "in get<T>()" in repr(excinfo)
    assert props["dict"]() == {"key": 42, "value": 3.14}
    assert props["dict"].as_object()() == {"key": 42, "value": 3.14}
    assert list(props["dict"].keys()) in [
        # order no guarantee (rapidjson has order, value(unordered_map) not)
        ["key", "value"],
        ["value", "key"],
    ]

    d = props["double"]
    assert d.GetType() == "double"
    assert d.Get() == d()
    assert isinstance(d(), float)
    with pytest.raises(RuntimeError) as excinfo:
        d.get("key")
    assert "in get<T>()" in repr(excinfo)
    assert d.set([1, 2, 3])() == [1, 2, 3]

    i = props["int"]
    assert i.GetType() == "uint64_t"
    assert i.GetUint64() == 42
    assert isinstance(i.GetUint64(), int)
    with pytest.raises(RuntimeError) as excinfo:
        i.GetInt64()
    assert "in get<T>()" in repr(excinfo)

    i = props["int2"]
    assert i.GetType() == "int64_t"
    assert i.GetInt64() == -101
    assert isinstance(i.GetInt64(), int)
    with pytest.raises(RuntimeError) as excinfo:
        i.GetUint64()
    assert "in get<T>()" in repr(excinfo)

    props["new"] = 6
    assert props["new"]() == 6
    props.from_rapidjson(rapidjson({"key": 6})).to_rapidjson()
    assert props() == {"key": 6}
    assert feature.properties()() == {"key": 6}
    assert feature.properties({"key": 7}).properties()() == {"key": 7}
    assert feature.properties(rapidjson({"key": 8})).properties()() == {
        "key": 8,
    }
    assert feature.geometry(geojson.Point(1, 2)).geometry()() == {
        "type": "Point",
        "coordinates": [1.0, 2.0, 0.0],
    }
    assert feature.geometry(geojson.Point(3, 4)).geometry().as_point()() == [
        3.0,
        4.0,
        0.0,
    ]
    assert (
        feature.to_rapidjson().dumps()
        == '{"type":"Feature","geometry":{"type":"Point","coordinates":[3.0,4.0,0.0]},"properties":{"key":8},"my_key":"my_value"}'
    )
    f2 = geojson.Feature().from_rapidjson(feature.to_rapidjson())
    assert f2 == feature
    assert f2() == feature()

    feature = geojson.Feature(sample_geojson())
    expected = '{"geometry":{"coordinates":[[120.4031748,31.41696608,1.111],[120.28451901,31.30578267,2.22],[120.35592249,31.21781896,3.333],[120.67093787,31.29950227,4.4]],"extra_key":"extra_value","type":"LineString"},"my_key":"my_value","properties":{"dict":{"key":42,"value":3.14},"double":3.142,"int":42,"int2":-101,"list":["a","list","is","a","list"],"string":"string"},"type":"Feature"}'
    assert feature.to_rapidjson().normalize().dumps() == expected
    assert normalize_json(feature.to_rapidjson()).dumps() == expected

    # adjust round_geojson_non_geometry
    assert feature.to_rapidjson().normalize()()["properties"]["double"] == 3.142
    assert (
        feature.to_rapidjson().normalize(round_geojson_non_geometry=1)()["properties"][
            "double"
        ]
        == 3.1
    )
    assert (
        feature.to_rapidjson().normalize(round_geojson_non_geometry=None)()[
            "properties"
        ]["double"]
        == 3.141592653
    )

    feature = geojson.Feature({**sample_geojson(), "id": 666})
    assert feature.id() == 666
    feature.clear()
    assert len(feature.properties()) == 0
    assert len(feature.custom_properties()) == 0
    assert feature() == {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": []},
        "properties": {},
    }
    assert feature.id() is None
    # id := variant<null, uint64, int64, double, string>
    assert feature.id(42).id() == 42
    assert feature.id(-1024).id() == -1024
    assert feature.id(3.14).id() == 3.14
    assert feature.id("string").id() == "string"
    assert feature.id(None).id() is None
    assert feature.id(-(2**63)).id() == -9223372036854775808
    assert feature.id(2**64 - 1).id() == 18446744073709551615
    with pytest.raises(RuntimeError) as excinfo:
        feature.id(2**64)  # out of range of uint64_t
    prefix = "integer out of range of int64_t/uint64_t"
    assert f"{prefix}: 18446744073709551616" in str(excinfo)
    feature["num"] = -(2**63)
    assert feature["num"]() == -9223372036854775808
    feature["num"] = 2**64 - 1
    assert feature["num"]() == 18446744073709551615
    with pytest.raises(RuntimeError) as excinfo:
        feature["num"] = 2**64
    assert f"{prefix}: 18446744073709551616" in str(excinfo)

    feature.clear()

    feature.id(2**63 - 1)
    pbf = feature.to_geobuf()
    assert feature.id() == 9223372036854775807
    assert geojson.Feature().from_geobuf(pbf).id() == 9223372036854775807
    text = pbf_decode(pbf)
    assert "12: 9223372036854775807" in text

    feature.id(2**63)
    pbf = feature.to_geobuf()
    assert feature.id() == 9223372036854775808
    assert geojson.Feature().from_geobuf(pbf).id() == 9223372036854775808
    text = pbf_decode(pbf)
    assert '11: "9223372036854775808"' in text

    feature.id(2**64 - 1)
    pbf = feature.to_geobuf()
    assert feature.id() == 18446744073709551615
    assert geojson.Feature().from_geobuf(pbf).id() == 18446744073709551615
    text = pbf_decode(pbf)
    assert '11: "18446744073709551615"' in text

    feature.id("text")
    pbf = feature.to_geobuf()
    assert feature.id() == "text"
    assert geojson.Feature().from_geobuf(pbf).id() == "text"
    text = pbf_decode(pbf)
    assert '11: "text"' in text

    feature.id(3.14)
    pbf = feature.to_geobuf()
    assert feature.id() == 3.14
    assert geojson.Feature().from_geobuf(pbf).id() == 3.14
    text = pbf_decode(pbf)
    assert '11: "3.14"' in text

    feature.id("3.14")
    pbf = feature.to_geobuf()
    assert feature.id() == "3.14"
    # note that not "3.14"
    assert geojson.Feature().from_geobuf(pbf).id() == 3.14
    text = pbf_decode(pbf)
    assert '11: "3.14"' in text

    assert feature["no_such_key"] is None
    feature["no_such_key"] = ["oops", {"it": "has"}]
    assert feature["no_such_key"] is not None
    assert feature["no_such_key"]() == ["oops", {"it": "has"}]
    assert feature.custom_properties()() == {
        "no_such_key": ["oops", {"it": "has"}],
    }
    del feature["no_such_key"]
    assert feature["no_such_key"] is None


def test_geojson_load_dump():
    dirname = os.path.abspath(f"{__pwd}/../data")
    path1 = os.path.join(dirname, "geometry.json")
    path2 = os.path.join(dirname, "feature.json")
    path3 = os.path.join(dirname, "feature_collection.json")
    json1 = rapidjson().load(path1)
    json2 = rapidjson().load(path2)
    json3 = rapidjson().load(path3)
    g = geojson.Geometry().from_rapidjson(json1)
    assert g.is_line_string()
    assert g.to_rapidjson() == json1
    f = geojson.Feature().from_rapidjson(json2)
    assert f.geometry() == g
    assert f.to_rapidjson() == json2
    assert f.id() == 234
    fc = geojson.FeatureCollection().from_rapidjson(json3)
    assert len(fc) == 1 and fc[0] == f
    assert fc.to_rapidjson() == json3

    for gg in [g, f, fc]:
        g0 = gg
        gg = gg.clone()
        assert len(gg.to_rapidjson().dumps()) > len(gg.round().to_rapidjson().dumps())
        assert len(gg.to_rapidjson().dumps()) == len(gg.round().to_rapidjson().dumps())
        assert len(gg.to_rapidjson().dumps()) > len(
            gg.round(lon=5, lat=5).to_rapidjson().dumps()
        )
        assert len(g0.to_rapidjson().dumps()) > len(gg.to_rapidjson().dumps())

    assert geojson.Geometry().load(path1) == g
    assert geojson.Feature().load(path2) == f
    assert geojson.FeatureCollection().load(path3) == fc

    g_ = geojson.GeoJSON().load(path1)
    assert g_.is_geometry()
    assert g_.as_geometry() == g
    assert g_()["type"] == "LineString"

    f_ = geojson.GeoJSON().load(path2)
    assert f_.is_feature()
    assert f_.as_feature() == f

    fc_ = geojson.GeoJSON().load(path3)
    assert fc_.is_feature_collection()
    assert fc_.as_feature_collection() == fc

    with pytest.raises(RuntimeError) as excinfo:
        geojson.GeoJSON().load("no_such_file")
    assert "can't open for reading: no_such_file" in repr(excinfo)

    path1 = os.path.join(dirname, "geometry.pbf")
    path2 = os.path.join(dirname, "feature.pbf")
    path3 = os.path.join(dirname, "feature_collection.pbf")

    g_ = geojson.GeoJSON().load(path1)
    assert g_.is_geometry()
    assert g.to_rapidjson() != g_.to_rapidjson()
    assert g.clone().round(lon=8, lat=8, alt=8).to_rapidjson() == g_.to_rapidjson()

    f_ = geojson.GeoJSON().load(path2)
    assert f_.is_feature()
    assert f_.as_feature().id() == 234
    assert f.to_rapidjson() != f_.to_rapidjson()
    assert f.clone().round(lon=8, lat=8, alt=8).to_rapidjson() == f_.to_rapidjson()

    fc_ = geojson.GeoJSON().load(path3)
    assert fc_.is_feature_collection()
    assert fc.to_rapidjson() != fc_.to_rapidjson()
    assert fc.clone().round(lon=8, lat=8, alt=8).to_rapidjson() == fc_.to_rapidjson()

    build_dir = os.path.abspath(f"{__pwd}/../build")
    os.makedirs(build_dir, exist_ok=True)
    path1 = f"{build_dir}/geometry.json"
    assert g.dump(path1, indent=True, sort_keys=True)
    assert geojson.GeoJSON().load(path1).as_geometry() == g
    path2 = f"{build_dir}/feature.json"
    assert f.dump(path2, indent=True, sort_keys=True)
    assert geojson.GeoJSON().load(path2).as_feature() == f
    path3 = f"{build_dir}/feature_collection.json"
    assert fc.dump(path3, indent=True, sort_keys=True)
    assert geojson.GeoJSON().load(path3).as_feature_collection() == fc

    path1 = f"{build_dir}/geometry.pbf"
    assert g_.dump(path1)
    assert geojson.GeoJSON().load(path1) == g_
    path2 = f"{build_dir}/feature.pbf"
    assert f_.dump(path2)
    assert geojson.GeoJSON().load(path2) == f_
    path3 = f"{build_dir}/feature_collection.pbf"
    assert fc_.dump(path3)
    assert geojson.GeoJSON().load(path3) == fc_

    # to/from_geobuf
    # (geojson keys may not in sorted order)
    decoded = geojson.GeoJSON().from_geobuf(g_.as_geometry().to_geobuf())
    assert decoded == g_

    decoded = geojson.GeoJSON().from_geobuf(f_.as_feature().to_geobuf())
    assert decoded == f_

    decoded = geojson.GeoJSON().from_geobuf(fc_.as_feature_collection().to_geobuf())
    assert decoded == fc_

    # onlyXY
    path1 = os.path.join(dirname, "geometry.json")
    path2 = os.path.join(dirname, "feature.json")
    path3 = os.path.join(dirname, "feature_collection.json")
    for path in [path1, path2, path3]:
        g = geojson.GeoJSON().load(path)
        g_xyz = geojson.GeoJSON().from_geobuf(g.to_geobuf())
        g_xy_ = geojson.GeoJSON().from_geobuf(g.to_geobuf(only_xy=True))
        if g.is_geometry():
            llas1 = g_xyz.as_geometry().as_numpy()
            llas2 = g_xy_.as_geometry().as_numpy()
        elif g.is_feature():
            llas1 = g_xyz.as_feature().as_numpy()
            llas2 = g_xy_.as_feature().as_numpy()
        else:
            llas1 = g_xyz.as_feature_collection()[0].as_numpy()
            llas2 = g_xy_.as_feature_collection()[0].as_numpy()
        assert np.all(llas1[:, :2] == llas2[:, :2])
        assert np.fabs(llas1[:, 2]).max() != 0.0
        assert np.fabs(llas2[:, 2]).max() == 0.0

    fc = geojson.FeatureCollection().from_rapidjson(json3)
    assert len(fc) == 1
    fc.append(fc[0])
    assert len(fc) == 2
    fc.append(fc[0])
    assert len(fc) == 3
    for i, f in enumerate(fc):
        f.properties()["int"] = f.properties()["int"]() * 100 + i
    fc["key"] = "value"
    assert fc.custom_properties()() == {"key": "value", "my_key": "this is fc"}
    del fc["my_key"]
    assert fc.custom_properties()() == {"key": "value"}
    assert [f.properties()["int"]() for f in fc] == [4200, 4201, 4202]
    del fc[:2]
    assert [f.properties()["int"]() for f in fc] == [4202]


def pytest_main(dir: str, *, test_file: str = None):
    os.chdir(dir)
    sys.exit(
        pytest.main(
            [
                dir,
                *(["-k", test_file] if test_file else []),
                "--capture",
                "tee-sys",
                "-vv",
                "-x",
            ]
        )
    )


@contextlib.contextmanager
def context_tempdir():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)


def test_rapidjson_dump_nan():
    j = rapidjson(
        {
            "key": "value",
            "pi": 3.14,
            "nan": np.nan,
        }
    )
    assert j.dumps() == '{"key":"value","pi":3.14,"nan":'
    assert j.locate_nan_inf() == '["nan"]'
    del j["nan"]
    assert j.locate_nan_inf() is None
    j["inf"] = np.inf
    assert j.locate_nan_inf() == '["inf"]'

    assert rapidjson(np.inf).locate_nan_inf() == ""
    assert rapidjson(np.nan).locate_nan_inf() == ""
    assert rapidjson("json").locate_nan_inf() is None

    jj = rapidjson({"root": {}})
    jj["root"]["child"] = j
    assert jj.locate_nan_inf() == '["root"]["child"]["inf"]'

    with context_tempdir() as dir:
        j = rapidjson({"root": {}})
        path = f"{dir}/okay.json"
        assert j.dump(path)
        with open(path) as f:
            text = f.read()
            assert text == '{"root":{}}'

    with context_tempdir() as dir:
        path = f"{dir}/fail.json"
        assert not jj.dump(path)


def test_rapidjson_normalize_non_geojson():
    j = normalize_json(rapidjson({"value": 3.14156}))
    assert j.dumps() == '{"value":3.142}'

    j = normalize_json(rapidjson({"value": 3.14156}), round_non_geojson=None)
    assert j.dumps() == '{"value":3.14156}'

    j = normalize_json(
        rapidjson(
            {
                "type": "Point",
                "coordinates": [1.23456, 7.890123, 4.567],
                "value": 3.123456,
            }
        ).sort_keys(),
        round_geojson_geometry=[3, 2, 1],
    )
    assert j.dumps() == '{"coordinates":[1.235,7.89,4.6],"type":"Point","value":3.123}'

    j = normalize_json(
        rapidjson(
            {
                "type": "Point",
                "coordinates": [1.23456, 7.890123, 4.567],
                "value": 3.123456,
            }
        ).sort_keys(),
        round_geojson_geometry=None,
    )
    assert (
        j.dumps()
        == '{"coordinates":[1.23456,7.890123,4.567],"type":"Point","value":3.123}'
    )

    j = normalize_json(
        rapidjson(
            {
                "type": "Point",
                "coordinates": [1.23456, 7.890123, 4.567],
                "value": 3.123456,
            }
        ).sort_keys(),
        round_geojson_geometry=[1, 1, 1],
        round_geojson_non_geometry=None,
    )
    assert j.dumps() == '{"coordinates":[1.2,7.9,4.6],"type":"Point","value":3.123456}'


def test_query():
    path = f"{__pwd}/../data/suzhoubeizhan.pbf"
    fc = geojson.FeatureCollection().load(path)
    planet = Planet(fc)

    tree = planet.packed_rtree()
    assert id(tree) == id(planet.packed_rtree())
    assert tree.extent.tolist() == [
        120.623512,
        31.4001743,
        120.67509,
        31.4458499,
    ]
    assert tree.num_items == 1016
    assert tree.num_nodes == 1085
    assert tree.node_size == 16

    hits = planet.query([120.64094, 31.41515], [120.64137, 31.41534])
    assert len(hits) == 4
    assert hits.tolist() == [529, 530, 536, 659]

    path = f"{__pwd}/../data/suzhoubeizhan_crossover.json"
    polygon = geojson.Feature().load(path).to_numpy()

    cropped1 = planet.crop(polygon[:, :2])
    cropped2 = planet.crop(polygon[:, :2], strip_properties=True)
    # cropped1.dump('cropped1.json', indent=True)
    # cropped2.dump('cropped2.json', indent=True)
    assert len(cropped1) == len(cropped2) == 54
    assert len(list(cropped1[0].properties().keys())) == 6
    assert list(cropped2[0].properties().keys()) == ["index"]
    assert cropped2[-1].properties()["index"]() == 977
    hits = [f.properties()["index"]() for f in cropped2]
    # assert fc[977] == cropped1[-1]


def test_geobuf_index():
    ipath = f"{__pwd}/../data/suzhoubeizhan.pbf"
    build_dir = os.path.abspath(f"{__pwd}/../build")
    os.makedirs(build_dir, exist_ok=True)
    opath = f"{build_dir}/suzhoubeizhan.idx"

    indexer = GeobufIndex()
    assert indexer.header_size == indexer.num_features == 0
    assert not indexer.offsets
    assert indexer.ids is None

    assert GeobufIndex.indexing(ipath, opath)

    # node bin/index2json build/suzhoubeizhan.idx > idx.json
    assert indexer.mmap_init(opath, ipath)
    assert indexer.header_size == 52
    assert indexer.num_features == 1016
    offsets = indexer.offsets
    assert len(offsets) == 1018
    assert offsets[:5] == [56, 318, 817, 999, 1174]
    assert indexer.ids["24"] == 0
    tree = indexer.packed_rtree
    assert id(tree) == id(indexer.packed_rtree)
    assert tree.extent.tolist() == [
        120.623512,
        31.4001743,
        120.67509,
        31.4458499,
    ]
    assert tree.num_items == 1016
    assert tree.num_nodes == 1085
    assert tree.node_size == 16

    expected = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [120.660822, 31.4001743, 0.0],
                [120.6610982, 31.4015175, 0.0],
                [120.6611093, 31.4015714, 0.0],
                [120.6612461, 31.4023039, 0.0],
                [120.661284, 31.4025068, 0.0],
                [120.6616616, 31.4042817, 0.0],
                [120.6618224, 31.4052508, 0.0],
                [120.6620808, 31.406731, 0.0],
                [120.6622092, 31.4073066, 0.0],
                [120.6623891, 31.4081988, 0.0],
                [120.6626607, 31.4095945, 0.0],
            ],
        },
        "properties": {
            "stroke": "#48fd6d",
            "folds": [
                [
                    "24",
                    "1870",
                    "40",
                    "1318",
                    "0",
                    "39",
                    "93",
                    "26",
                    "1224",
                    "2",
                ],
                [
                    151.228,
                    6.069,
                    82.252,
                    22.784,
                    200.044,
                    108.533,
                    165.949,
                    64.978,
                    100.392,
                    156.891,
                ],
            ],
            "highlight_group": ["23"],
            "prevs": [],
            "id": "24",
            "nexts": ["23"],
        },
    }
    assert indexer.decode_feature(0)() == expected
    f = indexer.decode_feature(0, only_geometry=True)()
    assert f["properties"] == {}
    f = indexer.decode_feature(0, only_properties=True)()
    assert f["geometry"] is None
    assert not indexer.decode_non_features()
    assert indexer.decode_non_features()() is None

    ipath = f"{__pwd}/../data/suzhoubeizhan.pbf"
    fc = geojson.GeoJSON().load(ipath)
    build_dir = os.path.abspath(f"{__pwd}/../build")
    os.makedirs(build_dir, exist_ok=True)
    opath = f"{build_dir}/suzhoubeizhan.pbf"
    fc.as_feature_collection()["number"] = 42
    fc.as_feature_collection()["string"] = "string"
    fc.as_feature_collection()["list"] = ["l", 1, "s", "t"]
    fc.as_feature_collection()["dict"] = {"d": "ict"}
    expected_custom_props = {
        "dict": {"d": "ict"},
        "list": ["l", 1, "s", "t"],
        "string": "string",
        "number": 42,
    }
    custom_props = fc.as_feature_collection().custom_properties()()
    assert custom_props == expected_custom_props
    assert fc.dump(opath) and os.path.isfile(opath)

    ipath = opath
    opath = f"{build_dir}/suzhoubeizhan.idx"
    assert GeobufIndex.indexing(ipath, opath)
    indexer = GeobufIndex()
    assert indexer.mmap_init(opath, ipath)
    assert indexer.decode_feature(0)() == expected
    assert indexer.decode_non_features()
    assert indexer.decode_non_features()() == expected_custom_props

    hits = indexer.query([120.64094, 31.41515], [120.64137, 31.41534])
    assert len(hits) == 4
    tree = indexer.packed_rtree
    assert sorted(hits) == sorted(
        tree.search(
            120.64094,
            31.41515,
            120.64137,
            31.41534,
        )
    )
    hits = [indexer.decode_feature(h) for h in hits]
    hits = [h.properties()["id"]() for h in hits]
    assert hits == ["943", "936", "937", "1174"]


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    pwd = os.path.abspath(os.path.dirname(__file__))
    pytest_main(pwd, test_file=os.path.basename(__file__))
