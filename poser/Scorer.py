import torch
import posenet
import numpy as np
import cv2


class Scorer():
	###
	# src_img and tgt_img should be processed cv2 images. (process_image util output)
	###
	def __init__(self, model=101, scale_factor=1.0):
		self.model = posenet.load_model(model)
		self.model = self.model.cuda()
		self.scale_factor = scale_factor

	def score_poses(self, src_f, tgt_f):
		src_KP_coordinates, src_overlay = self.get_KP_coordinates(src_f, True)
		tgt_KP_coordinates, _ = self.get_KP_coordinates(tgt_f) # do not draw overlay for target

		[src_x_ncoords, src_y_ncoords] = self.normalize_KP_coordinates(src_KP_coordinates)
		[tgt_x_ncoords, tgt_y_ncoords] = self.normalize_KP_coordinates(tgt_KP_coordinates)

		x_dist = src_x_ncoords - tgt_x_ncoords
		y_dist = src_y_ncoords - tgt_y_ncoords

		error = np.sqrt(np.square(x_dist) + np.square(y_dist))
		average_error = np.average(error)

		return average_error, src_overlay

	def normalize_KP_coordinates(self, coords):
		y_scale = np.max(coords[0, :, 0])
		x_scale = np.max(coords[0, :, 1])

		centre_y = coords[0, 0, 0]
		centre_x = coords[0, 0, 1]

		norm_y_coords = (coords[0, :, 0] - centre_y)/y_scale
		norm_x_coords = (coords[0, :, 1] - centre_x) / x_scale

		return [norm_x_coords, norm_y_coords]



	def get_KP_coordinates(self, f, src=False):
		output_stride = self.model.output_stride
		input_image, display_image, output_scale = posenet.utils._process_input(
            f, scale_factor=self.scale_factor, output_stride=output_stride)

		with torch.no_grad():
			input_image = torch.Tensor(input_image).cuda()
			heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = self.model(input_image)
			pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
                heatmaps_result.squeeze(0),
                offsets_result.squeeze(0),
                displacement_fwd_result.squeeze(0),
                displacement_bwd_result.squeeze(0),
                output_stride=output_stride,
                max_pose_detections=10,
                min_pose_score=output_stride)

			if src ==True:
				keypoint_coords *= output_scale
				overlay_image = posenet.draw_skel_and_kp(
        			f, pose_scores, keypoint_scores, keypoint_coords,)
				ret, jpeg = cv2.imencode('.jpg', overlay_image)
				out_f = jpeg.tobytes()
			else:
				out_f = None

		return keypoint_coords, out_f

if __name__ == "__main__":
	sr = Scorer()
	path = "C:\\Users\\micha\\PycharmProjects\\HtNPose\\frames\\"

	src = str(path+"frame0.jpg")
	tgt = str(path+"frame594.jpg")


	FINAL_SCORE = sr.score_poses(src, tgt)

	print(FINAL_SCORE)