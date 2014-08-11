from pandas import DataFrame
def virtexCAD():
	df = DataFrame.from_csv('marketHistory/virtexCAD.csv')
	return df