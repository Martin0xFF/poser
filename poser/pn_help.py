import posenet
import torch
import cv2
import base64
import numpy as np

class pose_estimator():
    def __init__(self, img_q, model=101, scale_factor=0.7125):
        self.model = posenet.load_model(model)
        self.model = self.model.cuda()
        self.output_stride = self.model.output_stride
        self.scale_factor = scale_factor
        self.latest = None
        self.img_q = img_q

    def infer_overlay(self,):
        current_img = self.img
        input_image, display_image, output_scale = posenet._process_input(
            self.img_q[0], scale_factor=self.scale_factor, output_stride=self.output_stride)

        with torch.no_grad():
            input_image = torch.Tensor(input_image).cuda()
            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = self.model(input_image)
            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
                heatmaps_result.squeeze(0),
                offsets_result.squeeze(0),
                displacement_fwd_result.squeeze(0),
                displacement_bwd_result.squeeze(0),
                output_stride=self.output_stride,
                max_pose_detections=10,
                min_pose_score=0.15)
        keypoint_coords *= output_scale

            # TODO this isn't particularly fast, use GL for drawing and display someday...
        overlay_image = posenet.draw_skel_and_kp(
        display_image, pose_scores, keypoint_scores, keypoint_coords,
        min_pose_score=0.15, min_part_score=0.1)
        ret, jpeg = cv2.imencode('.jpg', overlay_image)
        self.latest = jpeg.tobytes()
        return jpeg.tobytes()

def gen(queue):

    """
    When ever you call this, make sure to replace the current element of queue with
    """
    pe = pose_estimator(queue)

    while True:
        im_bytes = base64.b64decode(queue[0])
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        pe.img_q[0] = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

    yield