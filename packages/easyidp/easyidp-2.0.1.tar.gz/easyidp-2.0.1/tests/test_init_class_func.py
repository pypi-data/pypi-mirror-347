import re
import sys
import pytest
import numpy as np
import easyidp as idp

def test_class_container():
    # for i in c, 
    # for i in c.keys, 
    # for i in c.values, 
    # for i, j in c.items()
    ctn = idp.Container()

    k = [str(_) for _ in range(5)]

    v = []
    for _ in range(6, 11):
        p = idp.reconstruct.Photo()
        p.label = str(_)
        v.append(p)

    val = {}
    for i, j in zip(k,v):
        ctn[i] = j
        val[int(i)] = j
    
    assert ctn.id_item == val

    # test object iteration
    for idx, value in enumerate(ctn):
        assert value == v[idx]

    for idx, value in ctn.items():
        assert value in v

    for key in ctn.keys():  # [6,7,8,9,10]
        assert key in ['6','7','8','9','10']

    for value in ctn.values():
        assert value in v

    # test copy itself
    ctn_copy = ctn.copy()
    assert len(ctn_copy) == 5
    for key in ctn_copy.keys():  # [6,7,8,9,10]
        assert key in ['6','7','8','9','10']

    # test get order by slicing
    slice_test = ctn[0:3]

    assert len(slice_test) == 3
    for k in slice_test.keys():
        assert k in ['6', '7', '8']

def test_class_container_error():
    slice_test = idp.Container()
    slice_test['111'] = 111
    slice_test['222'] = 222
    slice_test['333'] = 333

    # test specify values without labels
    slice_test[0] = 4
    assert slice_test[0] == 4
    assert slice_test[1] == 222

    with pytest.raises(IndexError, match=re.escape("Index [4] out of range (0, 3)")):
        slice_test[4]

    with pytest.raises(IndexError, match=re.escape("Index [4] out of range (0, 3)")):
        slice_test[4] = 3

    with pytest.raises(KeyError, match=re.escape("Can not find key [233]")):
        slice_test['233']

    # spcify values with duplicate labels
    sensor1 = idp.reconstruct.Sensor()
    sensor2 = idp.reconstruct.Sensor()

    sensor1.id = 0
    sensor1.label = "FC1234"

    sensor2.id = 1
    sensor2.label = "FC1234"

    with pytest.raises(KeyError, match=re.escape("The given item's label [FC1234] already exists -> ")):
        duplicate_label_test = idp.Container()
        duplicate_label_test[sensor1.id] = sensor1
        duplicate_label_test[sensor2.id] = sensor2
    

def test_class_container_btf_print():
    # short container
    expected_str_s = '<easyidp.Container> with 3 items\n[0]\t1\narray([[1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.]], shape=(4, 3))\n[1]\t2\narray([[1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.]], shape=(4, 3))\n[2]\t3\narray([[1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.]], shape=(4, 3))'
    ctn = idp.Container()
    ctn['1'] = np.ones((4,3))
    ctn['2'] = np.ones((4,3))
    ctn['3'] = np.ones((4,3))

    assert ctn._btf_print().replace(' ', '') ==  expected_str_s.replace(' ', '')

    # long container
    expected_str_l = '<easyidp.Container> with 6 items\n[0]\t1\narray([[1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.]], shape=(4, 3))\n[1]\t2\narray([[1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.]], shape=(4, 3))\n...\n[4]\t134\narray([[1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.]], shape=(4, 3))\n[5]\t135\narray([[1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.],\n       [1., 1., 1.]], shape=(4, 3))'
    ctn['133'] = np.ones((4,3))
    ctn['134'] = np.ones((4,3))
    ctn['135'] = np.ones((4,3))

    assert ctn._btf_print().replace(' ', '') ==  expected_str_l.replace(' ', '')


def test_def_parse_photo_relative_path():

    if sys.platform.startswith("win"):
        frame_path = r"Z:\ishii_Pro\sumiPro\2022_soy_weeds_metashape_result\220613_G_M600pro\220613_G_M600pro.files\0\0\frame.zip"
        rel_path = r"../../../../source/220613_G_M600pro/DSC06093.JPG"
        actual_path = idp.parse_relative_path(frame_path, rel_path)
        expected_path = 'Z:\\ishii_Pro\\sumiPro\\2022_soy_weeds_metashape_result\\source\\220613_G_M600pro\\DSC06093.JPG'

        assert actual_path == expected_path

    else :
        frame_path = r"/ishii_Pro/sumiPro/2022_soy_weeds_metashape_result/220613_G_M600pro/220613_G_M600pro.files/0/0/frame.zip"
        rel_path = r"../../../../source/220613_G_M600pro/DSC06093.JPG"

        actual_path = idp.parse_relative_path(frame_path, rel_path)
        expected_path = r'/ishii_Pro/sumiPro/2022_soy_weeds_metashape_result/source/220613_G_M600pro/DSC06093.JPG'


def test_def_parse_photo_relative_path_warn():
    frame_path = r"Z:\ishii_Pro\sumiPro\2022_soy_weeds_metashape_result\220613_G_M600pro\220613_G_M600pro.files\0\0\frame.zip"
    rel_path = "//172.31.12.56/pgg2020a/drone/20201029/goya/DJI_0284.JPG"

    with pytest.warns(UserWarning, match=re.escape("Seems it is an absolute path")):
        get_path = idp.parse_relative_path(frame_path, rel_path)

    assert get_path == rel_path