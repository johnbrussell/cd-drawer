def get_precinct_order_dicts(
    df,
    unique_precinct_names,
    min_cd_size,
    precinct_number_dict,
    precinct_neighbor_dict,
    population_col,
):
    precinct_order_neighbors_dict = {}
    precinct_order_pop_dict = {}
    precinct_order_d_votes_dict = {}
    precinct_order_r_votes_dict = {}
    precinct_order_d_pct_dict = {}
    for precinct in unique_precinct_names:
        print(precinct)
        precinct_order_neighbors_dict[precinct] = {}
        precinct_order_pop_dict[precinct] = {}
        precinct_order_d_votes_dict[precinct] = {}
        precinct_order_r_votes_dict[precinct] = {}
        precinct_order_d_pct_dict[precinct] = {}

        order = 0
        latest_population = 0
        while latest_population < min_cd_size:
            # print(latest_population)
            neighborhood = {int(precinct_number_dict[precinct])}
            find_neighbors_order = 0
            previous_new_neighbors = {int(precinct_number_dict[precinct])}
            while find_neighbors_order < order:
                find_neighbors_order += 1
                new_neighbors = set()
                for n in previous_new_neighbors:
                    # print(precinct_neighbor_dict[186])
                    # print(n)
                    new_neighbors = new_neighbors.union(set(precinct_neighbor_dict[n]))
                new_neighbors = new_neighbors - neighborhood
                neighborhood = neighborhood.union(new_neighbors)
                previous_new_neighbors = new_neighbors

            # print(neighborhood)
            precinct_order_neighbors_dict[precinct][order] = neighborhood
            latest_population = df.loc[df["id_order"].isin(neighborhood), population_col].sum()
            precinct_order_pop_dict[precinct][order] = latest_population
            precinct_order_d_votes_dict[precinct][order] = df.loc[(df["id_order"].isin(neighborhood)), "PREDEM20,N,24,15"].sum()
            precinct_order_r_votes_dict[precinct][order] = df.loc[(df["id_order"].isin(neighborhood)), "PREREP20,N,24,15"].sum()
            precinct_order_d_pct_dict[precinct][order] = float(precinct_order_d_votes_dict[precinct][order]) / (precinct_order_d_votes_dict[precinct][order] + precinct_order_r_votes_dict[precinct][order])
            order += 1
            if not previous_new_neighbors:
                break

    return precinct_order_neighbors_dict, precinct_order_pop_dict, precinct_order_d_votes_dict, precinct_order_r_votes_dict, precinct_order_d_pct_dict
