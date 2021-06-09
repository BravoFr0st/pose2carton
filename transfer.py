#!/usr/bin/env python
# coding=utf-8

import os
import os.path as osp
import glob
import time
import warnings
import h5py
import argparse
import numpy as np

np.set_printoptions(suppress=True)
import open3d as o3d
import random
import pickle as pkl
from tqdm import tqdm
from obj_loader import TriangleMesh

eg = {0: 0, 1: 3, 2: 2, 3: 1, 4: 6, 5: 5, 6: 4, 7: 9, 8: 8, 9: 7}
Pose2 = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    18: 16,
    19: 17,
    20: 15,
    21: 18,
    22: 19,
    26: 20,
    27: 21,
}
Pose5 = {
    0: 0,
    1: 3,
    2: 1,
    3: 2,
    4: 6,
    5: 4,
    6: 5,
    7: 9,
    8: 7,
    9: 8,
    10: 14,
    11: 13,
    12: 12,
    13: 10,
    14: 11,
    15: 17,
    16: 16,
    17: 15,
    20: 19,
    21: 18,
    23: 21,
    24: 20,
}
Pose6 = {
    0: 0,
    2: 3,
    5: 6,
    6: 2,
    7: 1,
    9: 9,
    11: 5,
    12: 4,
    16: 13,
    19: 12,
    20: 14,
    23: 8,
    24: 7,
    28: 16,
    31: 15,
    32: 17,
    34: 11,
    37: 10,
    41: 18,
    46: 19,
    53: 20,
    58: 21,
}
Pose14 = {
    0: 0,
    1: 3,
    2: 1,
    3: 2,
    4: 6,
    5: 4,
    6: 5,
    7: 9,
    8: 7,
    9: 8,
    10: 12,
    11: 13,
    12: 14,
    13: 10,
    14: 11,
    15: 15,
    16: 16,
    17: 17,
    21: 18,
    22: 19,
    26: 20,
    27: 21,
}
Pose16 = {
    0: 0,
    1: 3,
    2: 2,
    3: 1,
    4: 6,
    5: 5,
    6: 4,
    7: 9,
    8: 8,
    9: 7,
    10: 12,
    11: 14,
    12: 13,
    13: 11,
    14: 10,
    15: 15,
    16: 17,
    17: 16,
    21: 19,
    22: 18,
    23: 21,
    24: 20,
}

Pose1 = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    17: 15,
    18: 16,
    19: 17,
    21: 18,
    22: 19,
    24: 20,
    25: 21,
    30: 22,
    35: 23,
}

fbx658 = {
    0: 0,
    3: 1,
    # 4: 3,
    6: 3,
    8: 2,
    # 9: 3,
    12: 4,
    15: 12,
    16: 14,
    17: 13,
    19: 5,
    21: 7,
    22: 15,
    23: 17,
    24: 16,
    25: 8,
    26: 10,
    27: 15,
    29: 19,
    30: 18,
    31: 11,
    33: 23,
    34: 22,
}
fbx674 = {
    0: 0,
    1: 1,
    2: 3,
    3: 2,
    8: 4,
    9: 12,
    11: 16,
    12: 17,
    13: 5,
    16: 7,
    17: 15,
    18: 18,
    19: 19,
    20: 8,
    22: 22,
    23: 23,
}
fbx1041 = {
    0: 0,
    1: 2,
    3: 1,
    4: 5,
    7: 13,
    8: 14,
    9: 12,
    10: 4,
    11: 8,
    14: 18,
    15: 19,
    16: 15,
    17: 7,
    18: 11,
    19: 18,
    20: 19,
    22: 10,
    23: 20,
    24: 21,
    26: 22,
    27: 22,
    28: 23,
    29: 23,
}
fbx3642 = {
    0: 0,
    1: 1,
    2: 3,
    3: 2,
    4: 4,
    5: 15,
    6: 17,
    7: 16,
    8: 5,
    11: 19,
    12: 18,
}
fbx8321 = {
    0: 0,
    1: 1,
    2: 6,
    3: 2,
    4: 4,
    5: 15,
    6: 17,
    7: 16,
    8: 5,
    11: 16,
    12: 17,
    9: 15,
    10: 15,
}
fbx8650 = {
    0: 0,
    1: 14,
    2: 3,
    3: 13,
    4: 3,
    5: 12,
    6: 17,
    7: 19,
    8: 4,
    9: 16,
    10: 18,
    11: 5,
    12: 15,
    13: 21,
    14: 8,
    15: 20,
    16: 7,
}
fbx9466 = {
    0: 0,
    2: 3,
    3: 2,
    4: 1,
    5: 12,
    6: 13,
    7: 14,
    8: 5,
    9: 4,
    10: 16,
    11: 17,
    12: 8,
    13: 7,
    14: 16,
    14: 18,
    15: 17,
    15: 19,
    16: 20,
    17: 21,
}
fbx9860 = {
    0: 0,
    1: 3,
    2: 0,
    3: 6,
    4: 1,
    5: 2,
    6: 16,
    7: 17,
    8: 12,
    9: 4,
    10: 5,
    11: 18,
    12: 19,
    13: 15,
    14: 7,
    15: 8,
    16: 20,
    17: 21,
}
fbx9870 = {
    0: 0,
    1: 1,
    2: 2,
    3: 6,
    4: 4,
    5: 5,
    6: 9,
    7: 7,
    8: 8,
    9: 16,
    10: 17,
    11: 12,
    12: 18,
    13: 19,
    14: 15,
    15: 20,
    16: 21,
    17: 15,
    18: 15,
    15: 22,
    16: 23,
}
fbx9878 = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 16,
    10: 17,
    11: 12,
    12: 18,
    13: 19,
    14: 15,
    15: 20,
    16: 21,
}
fbx10073 = {
    0: 0,
    1: 1,
    2: 3,
    3: 2,
    4: 4,
    5: 6,
    6: 5,
    7: 7,
    8: 12,
    9: 13,
    10: 14,
    11: 8,
    12: 10,
    13: 15,
    14: 16,
    15: 17,
    16: 11,
    19: 18,
    20: 19,
    22: 20,
    23: 21,
}
fbx11885 = {
    0: 0,
    1: 1,
    2: 3,
    3: 2,
    4: 4,
    5: 6,
    6: 5,
    7: 7,
    8: 12,
    10: 13,
    11: 14,
    12: 8,
    13: 10,
    14: 15,
    16: 16,
    18: 17,
    19: 11,
    24: 18,
    25: 19,
    26: 20,
    27: 21,
}
fbx12047 = {
    0: 0,
    1: 1,
    2: 3,
    3: 2,
    4: 4,
    5: 6,
    6: 5,
    7: 7,
    8: 12,
    9: 13,
    10: 14,
    11: 8,
    12: 10,
    13: 15,
    14: 16,
    15: 17,
    16: 11,
    17: 15,
    23: 18,
    24: 19,
    27: 20,
    28: 21,
    29: 22,
    30: 22,
    31: 23,
    32: 23,
    33: 22,
    34: 23,
}
fbx15596 = {
    0: 0,
    1: 1,
    2: 3,
    3: 2,
    4: 4,
    5: 6,
    6: 5,
    7: 7,
    8: 12,
    9: 13,
    10: 14,
    11: 8,
    12: 15,
    13: 16,
    14: 17,
    18: 18,
    19: 19,
    20: 20,
    21: 21,
}

smpl_joint_names = [
    "hips",  # 0
    "leftUpLeg",  # 1
    "rightUpLeg",  # 2
    "spine",  # 3
    "leftLeg",  # 4
    "rightLeg",  # 5
    "spine1",  # 6
    "leftFoot",  # 7
    "rightFoot",  # 8
    "spine2",  # 9
    "leftToeBase",  # 10
    "rightToeBase",  # 11
    "neck",  # 12
    "leftShoulder",  # 13
    "rightShoulder",  # 14
    "head",  # 15
    "leftArm",  # 16
    "rightArm",  # 17
    "leftForeArm",  # 18
    "rightForeArm",  # 19
    "leftHand",  # 20
    "rightHand",  # 21
    "leftHandIndex1",  # 22
    "rightHandIndex1",  # 23
]
loader_provided = "fbx/15596.txt"
loader_online = "./fbx/T-Pose1.txt"
# "fbx/T-Pose14.txt"
# ***** 需要补充的变量 ******
manual_model_to_smpl = Pose1
# (e.g.) manual_model_to_smpl = {0: 0, 1: 3, 2: 2, 3: 1, 4: 6, 5: 5, 6: 4, 7: 9, 8: 8, 9: 7, 10: 12, 11: 14, 12: 13, 21: 19, 22: 18, 23: 21, 24: 20, 16: 17, 17: 16}


def _lazy_get_model_to_smpl(_index2joint):
    """
    lazy mapper, which maps SMPL joints to character joints directly by their names
    """
    mappings = {}
    lower_smpl_joint_names = [name.lower() for name in smpl_joint_names]
    for index, joint_name in _index2joint.items():
        if joint_name.lower() not in lower_smpl_joint_names:
            continue
        smpl_index = lower_smpl_joint_names.index(joint_name.lower())
        mappings[index] = smpl_index
    return mappings


def _get_extra_uv_lines(infofile):
    """
    parse lines that contain uv coords and detailed face information from *file generated by mayapy*
    *if you do no use model downloaded elsewhere, you do not need to use this function*
    """
    infile = infofile.replace(".txt", "_intermediate.obj")
    assert osp.exists(
        infile
    ), "Can not find file {}, check whether you are using model downloaded from the internet. If so, run maya parser first".format(
        infile
    )
    lines = open(infile, "r").readlines()
    uv_lines = []
    for line in lines:
        line = line.strip("\n").strip()
        if "vt" in line or "mtl" in line or "f" in line or "vn" in line:
            uv_lines.append(line)
    return uv_lines


def clean_info(filename):
    """
    some fbx downloaded from the internet has strange pattern, clean that
    """
    with open(filename, "r") as f:
        content = f.read().strip()
    start = content.find("mix")
    end = content.find(":")
    if start == -1 or end == -1:
        return
    pattern = content[start : end + 1]
    # print(pattern)
    content = content.replace(pattern, "")
    with open(filename, "w") as f:
        f.write(content)
    print("clean finished")


def clean_obj(filename):
    """
    maya save fbx script need clean obj(mesh saved by open3d has unexpected comments and vertex colors, which is not supported by maya)
    """
    lines = open(filename, "r").readlines()
    lines = [line for line in lines if "#" not in line]
    out_lines = []
    for line in lines:
        line = line.strip("\n").strip()
        line = " ".join(line.split(" ")[:4])
        out_lines.append(line)

    with open(filename, "w") as f:
        f.write("\n".join(out_lines))


def forward_kinematics():
    pass


def with_zeros(x):
    return np.vstack((x, np.array([[0.0, 0.0, 0.0, 1.0]])))


def pack(x):
    return np.dstack((np.zeros((x.shape[0], 4, 3)), x))


def rodrigues(r):
    """
    util function which converts rotation vectors into rotation matrices
    """
    theta = np.linalg.norm(r, axis=(1, 2), keepdims=True)
    # avoid zero divide
    theta = np.maximum(theta, np.finfo(np.float64).eps)
    r_hat = r / theta
    cos = np.cos(theta)
    z_stick = np.zeros(theta.shape[0])
    m = np.dstack(
        [
            z_stick,
            -r_hat[:, 0, 2],
            r_hat[:, 0, 1],
            r_hat[:, 0, 2],
            z_stick,
            -r_hat[:, 0, 0],
            -r_hat[:, 0, 1],
            r_hat[:, 0, 0],
            z_stick,
        ]
    ).reshape([-1, 3, 3])
    i_cube = np.broadcast_to(np.expand_dims(np.eye(3), axis=0), [theta.shape[0], 3, 3])
    A = np.transpose(r_hat, axes=[0, 2, 1])
    B = r_hat
    dot = np.matmul(A, B)
    R = cos * i_cube + (1 - cos) * dot + np.sin(theta) * m
    return R


def transfer_given_pose(human_pose, infoname, is_root_rotated=False):
    """
    core function of human transfer, given human pose(24 x 3, rotation vectors), character rig info(.txt), character T-posed mesh(.obj), perform transfer 
    firstly parse rig info file and obtain the mapping from joint name to joint index and construct the kinematic chain
    secondly parse T-posed skeleton and skinning weight 
    thirdly use forward kinematics to transform T-posed skeleton into posed character skeleton 
    finally use blending weights to obtain posed mesh
    """
    lines = open(infoname).readlines()
    meshname = infoname.replace(".txt", ".obj")
    inmesh = o3d.io.read_triangle_mesh(meshname)
    v_posed = np.array(inmesh.vertices)

    custom_inmesh = TriangleMesh(meshname)
    inmesh.vertices = o3d.utility.Vector3dVector(custom_inmesh.vertices)
    inmesh.triangles = o3d.utility.Vector3iVector(custom_inmesh.triangles)
    v_posed = custom_inmesh.vertices

    hier = {}
    joint2index = {}
    index = 0
    # parse rig info file and obtain kinematic chain(hierarchical structure)
    for line in lines:
        line = line.strip("\n").strip()
        if line[:4] != "hier":
            continue
        splits = line.split(" ")
        parent_name = splits[1]
        child_name = splits[2]
        if parent_name not in joint2index:
            joint2index[parent_name] = index
            index += 1
        if child_name not in joint2index:
            joint2index[child_name] = index
            index += 1
        if parent_name not in hier:
            hier[parent_name] = [child_name]
        else:
            hier[parent_name].append(child_name)

    index2joint = {v: k for k, v in joint2index.items()}
    hier_index = {}
    for k, v in hier.items():
        hier_index[joint2index[k]] = [joint2index[vv] for vv in v]
    parents = list(hier_index.keys())
    children = []
    for v in hier_index.values():
        children.extend(v)
    root = [item for item in parents if item not in children]
    assert len(root) == 1
    root = root[0]

    # reorganize the index mapping to ensure that along each chain,
    # from root node to leaf node, the index number increases
    new_hier = {}
    new_joint2index = {index2joint[root]: 0}
    top_level = [root]
    index = 1
    for item in top_level:
        if item not in hier_index:
            # print('continue')
            continue
        for child in hier_index[item]:
            child_name = index2joint[child]
            if child_name not in new_joint2index:
                new_joint2index[child_name] = index
                index += 1
            if new_joint2index[index2joint[item]] not in new_hier:
                new_hier[new_joint2index[index2joint[item]]] = []
            new_hier[new_joint2index[index2joint[item]]].append(
                new_joint2index[child_name]
            )
            top_level.append(child)
    #print("joint names and their indices in the 3d character model")
    #print(new_joint2index)
    #print("kinetree table(kinematics connectivity) in the 3d character model")
    #print(new_hier)
    new_index2joint = {index: joint for joint, index in new_joint2index.items()}
    kinetree_table = [[-1, 0]]
    for k, v in new_hier.items():
        for vv in v:
            kinetree_table.append([k, vv])
    kinetree_table = np.array(kinetree_table).reshape(-1, 2).T

    # hierachical information, from which we can obtain kinematic chain
    hier_lines = [line for line in lines if "hier" in line]
    skin_lines = [line for line in lines if "skin" in line]
    num_joints = len(list(new_joint2index.keys()))
    num_vertices = len(skin_lines)
    # parse skinning weights from rig info file(.txt)
    weights = np.zeros((num_joints, num_vertices), dtype=np.float32)
    for line in skin_lines:
        line = line.strip().strip("\n")
        splits = line.split(" ")
        if len(splits) % 2 != 0:
            print("strange skin line found, please use other 3D models")
            return None, None

        vertex_index = int(splits[1])
        for i in range(2, len(splits), 2):
            joint_name = splits[i]
            weight = float(splits[i + 1])
            weights[new_joint2index[joint_name]][vertex_index] = weight

    # parse the T pose-skeleton
    joint_lines = [line for line in lines if "joints" in line and line[:6] == "joints"]
    joints = np.zeros((num_joints, 3), dtype=np.float32)
    for joint_line in joint_lines:
        joint_line = joint_line.strip().strip("\n")
        splits = joint_line.split(" ")
        name = splits[1]
        x = float(splits[2])
        y = float(splits[3])
        z = float(splits[4])
        joint_index = new_joint2index[name]
        joints[joint_index] = np.array([x, y, z])

    # child to index
    id_to_col = {kinetree_table[1, i]: i for i in range(kinetree_table.shape[1])}
    parent = {
        i: id_to_col[kinetree_table[0, i]] for i in range(1, kinetree_table.shape[1])
    }

    poses = np.zeros((1, num_joints, 3), dtype=np.float32)
    lazy_model_to_smpl = _lazy_get_model_to_smpl(new_index2joint)
    # if len(lazy_model_to_smpl) < 19:
    #     print("Please set mapping manually")
    #     return None, None

    # lazy mapper, directly match joints betwen SMPL and 3D character model by their names
    # if len(lazy_model_to_smpl) < 19:
    #     warn_info = "Lazy mapper can only map {} joints between 3D model and SMPL, you may map manually".format(len(lazy_model_to_smpl))
    #     print(warn_info)
    # print("lazy mapper and manual mapper obtains {}/{} joints respectively, choose the larger one".format(len(lazy_model_to_smpl), len(manual_model_to_smpl)))
    model_to_smpl = (
        lazy_model_to_smpl
        if len(lazy_model_to_smpl) > len(manual_model_to_smpl)
        else manual_model_to_smpl
    )

    # model_to_smpl = manual_model_to_smpl
    # ******* You need to perform mapping for at least 10 joints, otherwise you will receive this assertion ******
    assert (
        len(model_to_smpl) >= 10
    ), "Please map manually and ensure that at least 10 joints are matched"

    for model_index, smpl_index in model_to_smpl.items():
        if smpl_index == 0 and not is_root_rotated:
            continue
        poses[:, model_index] = human_pose[smpl_index]
    # print(joints.shape, kinetree_table.shape)
    # obtain rotation matrices from rotation vectors
    R = rodrigues(poses.reshape(-1, 1, 3))

    # forward kinematics process, calculate along the kinematic chain
    G = np.empty((kinetree_table.shape[1], 4, 4))
    G[0] = with_zeros(np.hstack((R[0], joints[0, :].reshape([3, 1]))))
    for i in range(1, kinetree_table.shape[1]):
        G[i] = G[parent[i]].dot(
            with_zeros(
                np.hstack(
                    [R[i], ((joints[i, :] - joints[parent[i], :]).reshape([3, 1]))]
                )
            )
        )
    new_joints = G[:, :3, 3]
    new_joint_lines = []
    for idx, name in enumerate(list(new_joint2index.keys())):
        new_joint_lines.append(
            "joints "
            + name
            + " {:.8f} {:.8f} {:.8f}".format(
                new_joints[idx, 0], new_joints[idx, 1], new_joints[idx, 2]
            )
        )

    # obtain joint offset from T-pose
    G = G - pack(
        np.matmul(
            G,
            np.hstack([joints, np.zeros([num_joints, 1])]).reshape([num_joints, 4, 1]),
        )
    )

    # linear blend skinning process, refer to SMPL paper for more details
    T = np.tensordot(weights.T, G, axes=[[1], [0]])
    rest_shape_h = np.hstack((v_posed, np.ones([v_posed.shape[0], 1])))
    v = np.matmul(T, rest_shape_h.reshape([-1, 4, 1])).reshape([-1, 4])[:, :3]

    root_line = ["root {}".format(new_index2joint[0])]
    out_lines = new_joint_lines + root_line + skin_lines + hier_lines
    outinfo = [line.strip("\n") for line in out_lines]
    outmesh = o3d.geometry.TriangleMesh(inmesh)
    outmesh.vertices = o3d.utility.Vector3dVector(v)

    # finally save the results for submission. Note that the logic here only saves connectivity. You still need to run vis.py to record visualization
    # if not osp.exists(osp.join("results", infoname.replace(".txt", ".pkl").replace('/', '_'))):
    os.makedirs("./results", exist_ok=True)
    save_dict = {
        "infoname": infoname,
        "hier": new_hier,
        "name2index": new_joint2index,
        "model2smpl": model_to_smpl,
    }
    with open(
        osp.join("results", str(infoname).replace(".txt", ".pkl").replace("/", "_")),
        "wb",
    ) as f:
        pkl.dump(save_dict, f)

    return outinfo, outmesh


def transfer_one_frame(infofile, use_online_model=False):
    """
    transfer human pose in one frame to 3D character
    infofile: riginfo file for one specific character model
    """
    np.random.seed(2021)
    # randomly sample one frame and obtain its pose
    with open("./pose_sample.pkl", "rb") as f:
        # poses shape: (N, 24, 3)
        poses = pkl.load(f)
    random_index = np.random.randint(0, len(poses))
    human_pose = poses[random_index]
    outinfo, outmesh = transfer_given_pose(human_pose, infofile)
    if use_online_model:
        extra_uv_lines = _get_extra_uv_lines(infofile)
    else:
        extra_uv_lines = None

    if outinfo is not None:
        out_infofile = infofile.split(".")[0] + "_" + str(random_index) + "_out.txt"
        out_objfile = infofile.split(".")[0] + "_" + str(random_index) + "_out.obj"
        with open(out_infofile, "w") as fp:
            fp.write("\n".join(outinfo))

        with open(out_objfile, "w") as fp:
            for v in np.asarray(outmesh.vertices):
                fp.write("v %f %f %f\n" % (v[0], v[1], v[2]))
            if use_online_model:
                # save texture uv coords and faces to
                for uv_line in extra_uv_lines:
                    fp.write(uv_line + "\n")
            else:
                # for f in np.asarray(outmesh.triangles) + 1:
                for f in np.asarray(outmesh.triangles):
                    fp.write("f %d %d %d\n" % (f[0], f[1], f[2]))
        print(
            "transferred finished, save to {} and {} with reference to human pose {}.obj".format(
                out_infofile, out_objfile, random_index
            )
        )


def transfer_one_sequence(infofile, seqfile, use_online_model=False):
    """
    transfer one sequence of human poses to 3D characters
    infofile: riginfo file for one specific character model 
    seqfile: sequence file that contains the sequential human pose
    """
    np.random.seed(2021)
    with open(seqfile, "rb") as f:
        human_poses = pkl.load(f)["pose"]
    savedir = seqfile.replace("info", "obj").split(".")[0] + "_3dmodel"
    os.makedirs(savedir, exist_ok=True)
    if use_online_model:
        extra_uv_lines = _get_extra_uv_lines(infofile)
        # create symlink
        for _file in os.listdir(os.path.dirname(infofile)):
            # for texture or material
            if (
                _file.endswith(".jpg")
                or _file.endswith(".mtl")
                or _file.endswith(".png")
            ):
                src_path = os.path.abspath(
                    os.path.join(os.path.dirname(infofile), _file)
                )
                dst_path = os.path.join(savedir, _file)
                if not osp.exists(dst_path):
                    os.symlink(src_path, dst_path)
    else:
        extra_uv_lines = None

    tbar = tqdm(range(len(human_poses)))
    for idx in tbar:
        human_pose = human_poses[idx]
        outinfo, outmesh = transfer_given_pose(
            human_pose, infofile, is_root_rotated=True
        )
        if outinfo is not None:
            out_infofile = osp.join(savedir, f"{idx}.txt")
            out_objfile = out_infofile.replace(".txt", ".obj")
            with open(out_infofile, "w") as fp:
                fp.write("\n".join(outinfo))
            with open(out_objfile, "w") as fp:
                for v in np.asarray(outmesh.vertices):
                    fp.write("v %f %f %f\n" % (v[0], v[1], v[2]))
                if use_online_model:
                    # save texture uv coords and faces to
                    for uv_line in extra_uv_lines:
                        fp.write(uv_line + "\n")
                else:
                    # for f in np.asarray(outmesh.triangles) + 1:
                    for f in np.asarray(outmesh.triangles):
                        fp.write("f %d %d %d\n" % (f[0], f[1], f[2]))
        else:
            print("map the 3D model to SMPL first, you can first try one frame setting")
            break


def parse_fbx(fbx_name):
    """
    parse fbx(downloaded from the internet) into mesh(.obj) and rig information(.txt, skinning weight, kinematic tree)
    refer to ./maya_fbx_parser.py for more details
    """
    fbx_files = (
        glob.glob(osp.join(fbx_name, "*.fbx")) if osp.isdir(fbx_name) else [fbx_name]
    )
    for fbx_file in tqdm(fbx_files):
        info_file = fbx_file.replace(".fbx", ".txt")
        obj_file = fbx_file.replace(".fbx", ".obj")
        if not osp.exists(info_file) or not osp.exists(obj_file):
            os.system("mayapy fbx_parser.py {} > /dev/null 2>&1".format(fbx_file))
        if not osp.exists(info_file) or not osp.exists(obj_file):
            print(
                "maya_fbx_parser: some error occurred, fail to extract {}".format(
                    info_file
                )
            )
            continue
        clean_info(info_file)
        # print('parse into {} and {}'.format(info_file, obj_file))


def save_fbx(info_files):
    """
    save rig info(.txt) and mesh(.obj) into fbx model, mesh file is found by replace suffix in rig info name
    refer to ./maya_save_fbx.py for more details
    """
    for info_file in info_files:
        os.system("mayapy maya_save_fbx.py {} > /dev/null 2>&1".format(info_file))
        if not osp.exists(info_file.replace(".txt", ".fbx")):
            print(
                "maya_save_fbx: some error occurred, fail to extract {}".format(
                    out_infoname.replace(".txt", "*.fbx")
                )
            )
            continue
        print("save to", info_file.replace(".txt", ".fbx"))


if __name__ == "__main__":

    # use fbx parser to paser fbx into obj, rig info (mayapy needed, you need to install and configure maya first)
    # parse_fbx("fbx")

    # infofiles = [osp.join("fbx", _file) for _file in os.listdir("fbx") if 'out' not in _file and _file.endswith(".txt")]
    # for infofile in infofiles:
    #     transfer_one_frame(infofile)

    # for provided models
    # transfer_one_frame(loader_provided)
    # transfer_one_sequence(loader_provided, "info_seq_5.pkl")

    # for possible model downloaded online
    clean_info(loader_online)
    transfer_one_frame(loader_online, use_online_model=True)
    transfer_one_sequence(loader_online, "info_seq_5.pkl", use_online_model=True)

