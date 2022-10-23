def addend(list, dict, value):
	if value not in dict:
		dict[value] = 1
	else:
		dict[value] += 1
	list.append(value)
	
def removestart(list, dict):
	if len(list) == 0:
		return None
	dict[list[0]] -= 1
	if dict[list[0]] == 0:
		del dict[list[0]]
	return list.pop(0)
	
def containshash(dict, value):
	if value in dict:
		return True
	return False