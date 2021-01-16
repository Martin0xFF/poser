import posenet
import torch
import cv2

class pose_estimator():
    def __init__(self, cap, model=101, scale_factor=0.7125):
        self.model = posenet.load_model(model)
        self.model = self.model.cuda()
        self.output_stride = self.model.output_stride
        self.cap = cap
        self.scale_factor = scale_factor




    def infer_overlay(self,):

        input_image, display_image, output_scale = posenet.read_cap(
            self.cap, scale_factor=self.scale_factor, output_stride=self.output_stride)

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
        return jpeg.tobytes()