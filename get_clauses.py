def is_inside(i:int,j:int)->bool:
    return (i>=0 and i<9 and j>=0 and j<9)

def dfs(i:int,j:int,map:list[list[int]],vis:list[list[int]],clauses:list):
    if(map[i][j]==-1 or vis[i][j]):
        return
    # perform dfs for cells atleast 2 cells away from me
    vis[i][j]=1     
    dir=[-2,-1,0,1,2]
    for d_x in dir:
        for d_y in dir:
            if(d_x==0 and d_y==0):
                continue
            if(is_inside(i+d_x,j+d_y)):
                dfs(i+d_x,j+d_y,map,vis,clauses)
    # if the cell contains a value add a clause
    if(map[i][j]>0):
        clause=[]
        dir_1=[-1,0,1]
        val=map[i][j]
        for d_x in dir_1:
            for d_y in dir_1:
                if(d_x==0 and d_y==0):
                    continue
                if(is_inside(i+d_x,j+d_y) and map[i+d_x][j+d_y]==-1):
                    clause.append([i+d_x,j+d_y])
                elif(is_inside(i+d_x,j+d_y) and map[i+d_x][j+d_y]==-2):
                    val-=1
        # print(i,j,':',clause,val)
        if(clause):
            clause.append(val)
            clauses.append(clause)

def get_connected_componenets_clauses(i:int,j:int,map:list[list[int]],vis:list[list[int]])->list[int]:
    clauses=[]
    dfs(i,j,map,vis,clauses)
    return clauses

def get_clauses(map:list[list]):
    # get the connected components and find the clauses expressions for each component, also specifying the component:
    vis=[[0]*9 for _ in range(9)]
    connected_components=0
    clauses=[]
    for i in range(0,9):
        for j in range(0,9):
            if(not vis[i][j] and map[i][j]!=-1):
               connected_components+=1
               clauses.append(get_connected_componenets_clauses(i,j,map,vis))
    return clauses