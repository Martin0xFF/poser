import json
import numpy as np


class score_keeper():
	def __init__(self):
		self.score = 0

	def calc_score(img1, img2):
		centrePoint = [0, 0]
		frameCount = -1
		avgErr = []

		for keyPointInd in range(1, numKeypoints):
			overallInd = frameInd*numKeypoints + keyPointInd
			tgtKP = targetKeypointsDiv[overallInd]
			srcKP = sourceKeypointsDiv[overallInd]

			tgtKPJSON = json.loads(tgtKP)
			srcKPJSON = json.loads(srcKP)


			xTgtList[keyPointInd] = (tgtKPJSON["xCoord"] - tgtCentre[0])
			xSrcList[keyPointInd] = (srcKPJSON["xCoord"] - srcCentre[0])


			yTgtList[keyPointInd] = (tgtKPJSON["yCoord"] - tgtCentre[1])
			ySrcList[keyPointInd] = (srcKPJSON["yCoord"] - srcCentre[1])

		NormedXTgtList = xTgtList / np.max(np.abs(xTgtList))
		NormedYTgtList = yTgtList / np.max(np.abs(yTgtList))

		NormedXSrcList = xSrcList / np.max(np.abs(xSrcList))
		NormedYSrcList = ySrcList / np.max(np.abs(ySrcList))

		xDist = NormedXTgtList - NormedXSrcList
		yDist = NormedYTgtList - NormedYSrcList

		err = np.sqrt(xDist**2 + yDist**2)

		print(np.average(err))
