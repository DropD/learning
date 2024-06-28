cfold' func init [] = init
cfold' func init (first:rest) = func first init (\init_ -> cfold' func init_ rest)

cfold func init lst = cfold' (\first_ init_ cont_ -> func first_ (cont_ init_)) init lst

cmap' func [] = []
cmap' func (first:rest) = func first : (cmap' func rest)
