def print_star(rows):
    i1= rows
    while i1 >=1:
        j1=1
        while  j1<=i1:
            print(i1,end=" ")
            j1=j1+1
        print()
        i1=i1-1

rows=int(input("Enter no of rows:"))

print_star(rows)
