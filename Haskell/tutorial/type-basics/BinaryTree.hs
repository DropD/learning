module BinaryTree
    where

data BinaryTree a 
    = Leaf a
    | Branch (BinaryTree a) a (BinaryTree a)

testTree = Branch (Leaf 2) 1 (Branch (Leaf 4) 3 (Leaf 5))

treeSize :: BinaryTree a -> Int
treeSize (Leaf _) = 1
treeSize (Branch left _ right) = 1 + treeSize left + treeSize right

elements :: BinaryTree a -> [a]
elements (Leaf value) = [value]
elements (Branch left value right) = elements left ++ [value] ++ elements right

treeFoldr :: (a -> b -> b) -> b -> BinaryTree a -> b
treeFoldr func init (Leaf value) = func value init
treeFoldr func init (Branch left value right) = 
    let fold_to_right = treeFoldr func init right in
    treeFoldr func (func value fold_to_right) left

elements2 :: BinaryTree a -> [a]
elements2 = treeFoldr (:) []

{-
        a
       / \
      b   c
     / \
    d   e

    -> func d (func b (func e (func a (func c init) ) ) )
 -}

treeFoldl :: (b -> a -> b) -> b -> BinaryTree a -> b
treeFoldl func init (Leaf value) = func init value
treeFoldl func init (Branch left value right) =
  treeFoldl func (func (treeFoldl func init left) value) right
append a b = a ++ [b]
elements3 :: BinaryTree a -> [a]
elements3 = treeFoldl append []
