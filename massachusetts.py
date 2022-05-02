from libpysal.weights import Rook
import pandas as pd
import numpy as np


w_rook = Rook.from_shapefile("shapefiles/WARDSPRECINCTS_POLY.shp")

# print(w_rook.component_labels)  # just 0s
# print(w_rook.id_order)  # 0 to 2151 in order

# print(type(w_rook))  type is Rook
# print(w_rook.neighbors)  # is a dictionary

shapefile_info = pd.read_csv("shapefiles/precinct_dbf_info.csv")
results_info = pd.read_csv("ma-senate-2018-precinct-results.csv")

shapefile_info["id_order"] = range(0, len(shapefile_info))

# print(shapefile_info[:5])
# print(results_info[:5])

df = pd.merge(results_info, shapefile_info, left_on=["jurisdiction_name", "precinct"], right_on=["TOWN,C,35", "DISTRICT,C,10"])
# print(df[:5])
#
# print(len(df))
# print(len(shapefile_info))
# print(len(results_info))

df["precinct_name"] = df["jurisdiction_name"] + "-" + df["precinct"]
# print(df["precinct_name"][:5])

# print(df[["precinct_name", "id_order", "candidate", "votes"]])

unique_precinct_names = df["precinct_name"].unique()
precinct_neighbor_dict = w_rook.neighbors
precinct_number_dict = dict(zip(df["precinct_name"], df["id_order"]))

total_population = sum(df.loc[df["precinct_name"] == precinct, "POP_2010,N,10,0"].max() for precinct in unique_precinct_names)

MIN_MA_CD_SIZE = total_population / 9 * 0.998

precinct_order_neighbors_dict = {}
precinct_order_pop_dict = {}
precinct_order_d_votes_dict = {}
precinct_order_r_votes_dict = {}
precinct_order_d_pct_dict = {}
for precinct in unique_precinct_names:
    # print(precinct)
    precinct_order_neighbors_dict[precinct] = {}
    precinct_order_pop_dict[precinct] = {}
    precinct_order_d_votes_dict[precinct] = {}
    precinct_order_r_votes_dict[precinct] = {}
    precinct_order_d_pct_dict[precinct] = {}

    order = 0
    latest_population = 0
    while latest_population < MIN_MA_CD_SIZE:
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
        latest_population = df.loc[df["id_order"].isin(neighborhood) & (df["party_detailed"] == "DEMOCRAT"), "POP_2010,N,10,0"].sum()
        precinct_order_pop_dict[precinct][order] = latest_population
        precinct_order_d_votes_dict[precinct][order] = df.loc[(df["id_order"].isin(neighborhood)) & (df["party_detailed"] == "DEMOCRAT"), "votes"].sum()
        precinct_order_r_votes_dict[precinct][order] = df.loc[(df["id_order"].isin(neighborhood)) & (df["party_detailed"] == "REPUBLICAN"), "votes"].sum()
        precinct_order_d_pct_dict[precinct][order] = float(precinct_order_d_votes_dict[precinct][order]) / (precinct_order_d_votes_dict[precinct][order] + precinct_order_r_votes_dict[precinct][order])
        order += 1
        if not previous_new_neighbors:
            break

# print(precinct_order_d_pct_dict)

order_dict = {}
order = 0
while True:
    total_neighborhoods = len([1 for precinct, orders in precinct_order_d_pct_dict.items() if order in orders])
    if total_neighborhoods == 0:
        break
    total_d = len([1 for precinct, orders in precinct_order_d_pct_dict.items() if order in orders and orders[order] > 0.5])
    total_r = len([1 for precinct, orders in precinct_order_d_pct_dict.items() if order in orders and orders[order] < 0.5])
    pct_d = total_d / float(total_r + total_d)
    avg_size = np.mean([len(orders[order]) for precinct, orders in precinct_order_neighbors_dict.items() if order in orders])
    avg_pop = np.mean([orders[order] for precinct, orders in precinct_order_pop_dict.items() if order in orders])
    avg_d_votes = np.mean([orders[order] for precinct, orders in precinct_order_d_votes_dict.items() if order in orders])
    avg_r_votes = np.mean([orders[order] for precinct, orders in precinct_order_r_votes_dict.items() if order in orders])
    order_dict[order] = {
        "Total": total_neighborhoods,
        "Avg. size": avg_size,
        "Avg. population": avg_pop,
        "Avg. D votes": avg_d_votes,
        "Avg. R votes": avg_r_votes,
        "D": total_d,
        "R": total_r,
        "Pct": pct_d,
    }
    order += 1

for order, od in order_dict.items():
    print(order)
    print(od)

precinct_data_dict = {}
for precinct in unique_precinct_names:
    max_order = max([o for o in precinct_order_d_pct_dict[precinct].keys()])
    population = precinct_order_pop_dict[precinct][max_order]
    if population < MIN_MA_CD_SIZE:
        continue
    num_neighbors = len(precinct_order_neighbors_dict[precinct][max_order])
    d_votes = precinct_order_d_votes_dict[precinct][max_order]
    r_votes = precinct_order_r_votes_dict[precinct][max_order]
    d_pct = d_votes / (d_votes + r_votes)
    precinct_data_dict[precinct] = {
        "Num neighbors": num_neighbors,
        "Population": population,
        "D": d_votes,
        "R": r_votes,
        "Pct": d_pct,
    }

print("Avg. num neighbors: ", np.mean([pd["Num neighbors"] for pd in precinct_data_dict.values()]))
print("Avg. population: ", np.mean([pd["Population"] for pd in precinct_data_dict.values()]))
print("Avg. D: ", np.mean([pd["D"] for pd in precinct_data_dict.values()]))
print("Avg. R: ", np.mean([pd["R"] for pd in precinct_data_dict.values()]))
print("Avg. D pct: ", np.mean([pd["Pct"] for pd in precinct_data_dict.values()]))
print("Num D: ", len([pd for pd in precinct_data_dict.values() if pd["Pct"] > 0.5]))
print("Num R: ", len([pd for pd in precinct_data_dict.values() if pd["Pct"] < 0.5]))
print("Num even: ", len([pd for pd in precinct_data_dict.values() if pd["Pct"] == 0.5]))

r_precincts = {precinct: pd for precinct, pd in precinct_data_dict.items() if pd["Pct"] < 0.5}
for precinct, pd in r_precincts.items():
    print(precinct, pd)
