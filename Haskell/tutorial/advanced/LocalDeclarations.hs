module LocalDeclarations
  where

-- let bindings
polyLet a = 
  let a2 = a * a
      a3 = a * a2
   in 5 * a + 7 * a2 - a3

-- where clause
polyWhere a =
  5 * a + 7 * a2 - a3  
  where a2 = a * a
        a3 = a * a2

-- mixing let and where
-- NEVER
-- EVER
-- DO THIS!!!!!!
polyMixed a = 
  let a2 = a * a
   in 5 * a + 7 * a2 - a3
  where a2 = 2 * a -- shadowed by a2 in the let
        a3 = a * a * a / 8
