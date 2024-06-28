module Types
    where

data Pair a b = Pair a b

pairFst (Pair x y) = x
pairSnd (Pair x y) = y


data Triple a b c = Triple a b c
tripleFst (Triple a _ _) = a
tripleSnd (Triple _ b _) = b
tripleThr (Triple _ _ c) = c


data Quad a b = Quad a a b b

firstTwo :: Quad a b -> [a]
firstTwo (Quad a b _ _) = [a, b]

secondTwo :: Quad a b -> [b]
secondTwo (Quad _ _ a b) = [a, b]


-- Multiple constructors
--

{-
 - data Maybe a = Nothing | Just a
 - 
 - is defined in Prelude
 -}
firstElement :: [a] -> Maybe a
firstElement [] = Nothing
firstElement (x : rest) = Just x

findElement :: (a -> Bool) -> [a] -> Maybe a
findElement predicate [] = Nothing
findElement predicate (item : rest) =
    if predicate item
        then Just item
    else findElement predicate rest

{-
 - Tuple exercise
 -}
data Tuple a b c d = Singlet a | Doublet a b | Triplet a b c | Quadruplet a b c d

tuple1 (Singlet a) = Just a
tuple1 (Doublet a _) = Just a
tuple1 (Triplet a _ _) = Just a
tuple1 (Quadruplet a _ _ _) = Just a

tuple2 (Singlet _) = Nothing
tuple2 (Doublet _ b) = Just b
tuple2 (Triplet _ b _) = Just b
tuple2 (Quadruplet _ b _ _) = Just b

tuple3 (Singlet _) = Nothing
tuple3 (Doublet _ _) = Nothing
tuple3 (Triplet _ _ c) = Just c
tuple3 (Quadruplet _ _ c _) = Just c

tuple4 (Singlet _) = Nothing
tuple4 (Doublet _ _) = Nothing
tuple4 (Triplet _ _ _) = Nothing
tuple4 (Quadruplet _ _ _ d) = Just d


-- Recursive Datatypes
--

data List a = Nil | Cons a (List a)
listLength Nil = 0
listLength (Cons item rest) = 1 + listLength rest

{-
 - List exercise
 -}
listHead :: List a -> a
listHead (Cons first rest) = first

listTail :: List a -> a
listTail (Cons last Nil) = last
listTail (Cons first rest) = listTail rest

listFoldl :: (b -> a -> b) -> b -> List a-> b
listFoldl function init Nil = init
listFoldl function init (Cons first rest) = listFoldl function (function init first) rest

listFoldr :: (a -> b -> b) -> b -> List a-> b
listFoldr function init Nil = init
listFoldr function init (Cons first rest) = function first (listFoldr function init rest)

-- foldl (-) 1 testref == listFoldl (-) 1 testlist == 1
-- foldr (-) 1 testref == listFoldr (-) 1 testlist == 5
testlist = Cons 2 (Cons (-2) Nil)
testref = [2, -2]
