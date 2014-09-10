#sufficient condition for hamiltonicity
def is_dirac(g):
    n = g.order()
    deg = g.degree()
    delta=min(deg)
    if n/2 <= delta:
        return True
    else:
        return False

#sufficient condition for hamiltonicity
def is_ore(g):
    A = g.adjacency_matrix()
    D = g.degree()
    n = g.order()
    for i in range(n):
        for j in range(i):
            if A[i][j]==0:
                if D[i] + D[j] < n:
                    return False
    return True

#sufficient condition for hamiltonicity
def is_haggkvist_nicoghossian(g):
    k = g.vertex_connectivity()
    n = g.order()
    delta = min(g.degree())
    if k >= 2 and delta >= (1.0/3)*(n+k):
        return True
    else:
        return False

#sufficient condition for hamiltonicity
def is_fan(g):
    k = g.vertex_connectivity()
    if k < 2:
        return False
    D = g.degree()
    Dist = g.distance_all_pairs()
    V = g.vertices()
    n = g.order()
    for i in range(n):
        for j in range (i):
            if Dist[V[i]][V[j]]==2 and max(D[i],D[j]) < n/2.0:
                return False
    return True

#sufficient condition for hamiltonicity
def is_planar_transitive(g):
    if g.order() > 2 and g.is_planar() and g.is_vertex_transitive():
        return True
    else:
        return False

def neighbors_set(g,S):
    N = set()
    for v in S:
        for n in g.neighbors(v):
            N.add(n)
    return list(N)

#sufficient condition for hamiltonicity
def is_generalized_dirac(g):
    n = g.order()
    k = g.vertex_connectivity()
    if k < 2:
        return False
    for p in Subsets(g.vertices(),2):
        if g.is_independent_set(p):
            if len(neighbors_set(g,p)) < (2.0*n-1)/3:
                return False
    return True

#necessary condition for hamiltonicity
def is_van_den_heuvel(g):
    n = g.order()
    lc = sorted(graphs.CycleGraph(n).laplacian_matrix().eigenvalues())
    lg = sorted(g.laplacian_matrix().eigenvalues())

    for lci, lgi in zip(lc, lg):
        if lci > lgi:
            return False

    def Q(g):
        A = g.adjacency_matrix()

        D = A.parent(0)

        if A.is_sparse():
            row_sums = {}
            for (i,j), entry in A.dict().iteritems():
                row_sums[i] = row_sums.get(i, 0) + entry
            for i in range(A.nrows()):
                D[i,i] += row_sums.get(i, 0)
        else:
            row_sums=[sum(v) for v in A.rows()]
            for i in range(A.nrows()):
                D[i,i] += row_sums[i]

        return D + A

    qc = sorted(Q(graphs.CycleGraph(n)).eigenvalues())
    qg = sorted(Q(g).eigenvalues())

    for qci, qgi in zip(qc, qg):
        if qci > qgi:
            return False

    return True

#necessary condition for hamiltonicity
def is_two_connected(g):
    k = g.vertex_connectivity()
    if k < 2:
        return False
    else:
        return True

#sufficient condition for hamiltonicity
def is_lindquester(g):
    k = g.vertex_connectivity()
    if k < 2:
        return False
    D = g.distance_all_pairs()
    n = g.order()
    V = g.vertices()
    for i in range(n):
        for j in range(i):
            if D[V[i]][V[j]] == 2:
                if len(neighbors_set(g,[V[i],V[j]])) < (2*n-1)/3.0:
                    return False
    return True

def is_complete(g):
    n = g.order()
    e = g.size()
    if not g.has_multiple_edges():
        return e == n*(n-1)/2

    D = g.distance_all_pairs()
    for i in range(n):
        for j in range(i):
            if D[V[i]][V[j]] != 1:
                return False
    return True

def has_claw(g):
    return g.subgraph_search(graphs.ClawGraph(), induced=True) is not None

def is_claw_free(g):
    return not has_claw(g)

def has_perfect_matching(g):
    n = g.order()
    if n%2 == 1:
        return False
    nu = g.matching(value_only=True)
    if 2*nu == n:
        return True
    else:
        return False

#true if radius equals diameter
def has_radius_equal_diameter(g):
    return g.radius() == g.diameter()

#true if residue equals independence number
def has_residue_equals_alpha(g):
    return residue(g) == independence_number(g)

def is_not_forest(g):
    return not g.is_forest()


def bipartite_double_cover(g):
    return g.tensor_product(graphs.CompleteGraph(2))

def closed_neighborhood(g, verts):
        if isinstance(verts, list):
            neighborhood = []
            for v in verts:
                neighborhood += [v] + g.neighbors(v)
            return list(set(neighborhood))
        else:
            return [verts] + g.neighbors(verts)

#has no non-empty critical independent set (<=> the only solution to the LP independence number relaxation is all 1/2's)
def has_empty_KE_part(g):
    b = bipartite_double_cover(g)
    alpha = b.order() - b.matching(value_only=True)
    for v in g.vertices():
        test = b.copy()
        test.delete_vertices(closed_neighborhood(b,[(v,0), (v,1)]))
        alpha_test = test.order() - test.matching(value_only=True) + 2
        if alpha_test == alpha:
            return False
    return True

# Vizing's Theorem: chromatic index of any graph is either Delta or Delta+1
def is_class1(g):
    if chromatic_index(g) == max(g.degree()):
        return True
    else:
        return False

def is_class2(g):
    if chromatic_index(g) == max(g.degree()):
        return False
    else:
        return True

def is_cubic(g):
    D = g.degree()
    if min(D) == 3 and max(D) == 3:
        return True
    else:
        return False

#a property that applied to all entered hamiltonian graphs but not the tuttle graph, false for tutte graph
def is_anti_tutte(g):
    if not g.is_connected():
        return False
    if independence_number(g) <= g.diameter() + g.girth():
        return True
    else:
        return False

#for any graph diam <= 2*radius. this property is true in the extremal case
def diameter_equals_twice_radius(g):
    if not g.is_connected():
        return False
    if g.diameter() == 2*g.radius():
        return True
    else:
        return False

efficiently_computable_properties = [Graph.is_regular, Graph.is_planar, Graph.is_forest, Graph.is_eulerian, Graph.is_connected, Graph.is_clique, Graph.is_circular_planar, Graph.is_chordal, Graph.is_bipartite, Graph.is_cartesian_product, Graph.is_distance_regular,  Graph.is_even_hole_free, Graph.is_gallai_tree, Graph.is_line_graph, Graph.is_overfull, Graph.is_perfect, Graph.is_split, Graph.is_strongly_regular, Graph.is_triangle_free, Graph.is_weakly_chordal, is_dirac, is_ore, is_haggkvist_nicoghossian, is_generalized_dirac, is_van_den_heuvel, is_two_connected, is_lindquester, is_claw_free, has_perfect_matching, has_radius_equal_diameter, is_not_forest, has_empty_KE_part, is_fan, is_cubic, diameter_equals_twice_radius]

intractable_properties = [Graph.is_hamiltonian, Graph.is_vertex_transitive, Graph.is_edge_transitive, has_residue_equals_alpha, Graph.is_odd_hole_free, Graph.is_semi_symmetric, Graph.is_line_graph, is_planar_transitive, is_class1, is_class2, is_anti_tutte ]

properties = efficiently_computable_properties + intractable_properties

# Graph.is_prime removed as faulty 9/2014
# built in Graph.is_transitively_reduced removed 9/2014
# is_line_graph is theoretically efficient - but Sage's implementation is not 9/2014

# weakly_chordal = weakly chordal, i.e., the graph and its complement have no induced cycle of length at least 5
