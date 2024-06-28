module PointFree
  where

{-
   pow could be written as

   pow base exp = foldr (*) 1 (replicate exp base)
   > pow 2 7
   > 127
   -}
pow = curry $ (foldr (*) 1) . (uncurry $ flip $ replicate)


-- func1 x l = map (\y -> y * x) l
func1_eta x = map (\y -> y * x)
func1_comp x = map (*x)
func1 = 
