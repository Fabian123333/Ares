import json
from bson import json_util

def parseJson(out):
	if type(out) == list:
		ret = []
		for o in out:
			ret.append(json.loads(o.toJSON()))
	else:
		ret = json.loads(out.toJSON())
	return json.loads(json_util.dumps(ret,default=json_util.default))

def parseOutput(out):
	if "_id" in out:
		out["id"] = str(out["_id"])
		del out["_id"]
	
	if(type(out) == dict):
		for k, v in out.items():
			if "_id" in v:
				out[k]["id"] = str(v["_id"])
				del out[k]["_id"]

	if(type(out) == list):
		o = out
		out = []
		
		for j in o:	
			if "_id" in j:
				j["id"] = str(j["_id"])
				del j["_id"]			
			out.append(j)
	
	return json.loads(json_util.dumps(out,default=json_util.default))

def shrinkJson(data):
	value = dict()
	for k, v in vars(data).items():
		if v != None and k != "exist":
			value[k] = v
	return value