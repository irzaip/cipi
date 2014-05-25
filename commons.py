
def map(x, in_min, in_max, out_min, out_max):
  myresult = (float(x) - float(in_min)) * (float(out_max) - float(out_min)) / (float(in_max) - float(in_min)) + float(out_min)
  return round(myresult,2)
  
  