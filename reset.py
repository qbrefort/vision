from naoqi import ALProxy


# We use the "Body" name to signify the collection of all joints
def reset_nao(IP):
	pNames = "Body"
	pStiffnessLists = 0.0
	pTimeLists = 1.0
	proxy = ALProxy("ALMotion", IP, 9559)
	proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

