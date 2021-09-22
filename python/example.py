from graph import Graph, UnitNode


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)


def insertion_sort(nums):
    if nums == []:
        return None
    head = Node(nums.pop())
    for num in nums:
        curr = head
        prev = None
        new_node = Node(num)
        if num <= curr.data:
            new_node.next = head
            head = new_node
            continue
        while curr is not None and num > curr.data:
            g = Graph(head)
            un = UnitNode(num)
            g.add(un)
            g.connect(un, curr)
            s = g.draw(node_colour_func=lambda n: "red" if n == curr else "green" if n == un else "blue")
            prev = curr
            curr = curr.next
        prev.next = new_node
        new_node.next = curr
    return head


nums = [2, 5, 1, 5, 7, 1, 52, 7, 13]
g = Graph(insertion_sort(nums))
print("done")