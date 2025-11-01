import pandas as pd
from math import radians, sin, cos, atan2, sqrt

# small city coords map (used only for distance estimation between warehouses)
city_coords = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714)
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def assign_coords(df):
    df = df.copy()
    df['Lat'] = df['Location'].map(lambda c: city_coords.get(c, (20.5937,78.9629))[0])
    df['Lon'] = df['Location'].map(lambda c: city_coords.get(c, (20.5937,78.9629))[1])
    return df

def compute_surplus_deficit(df_inventory):
    # group by Warehouse and Product_Category
    grp = df_inventory.groupby(['Warehouse_ID','Location','Product_Category']).agg(
        Current_Stock_Units=('Current_Stock_Units','sum'),
        Reorder_Level=('Reorder_Level','mean'),
        Storage_Cost_per_Unit=('Storage_Cost_per_Unit','mean')
    ).reset_index()
    # compute delta = current - reorder; positive = surplus, negative = deficit
    grp['Delta'] = grp['Current_Stock_Units'] - grp['Reorder_Level']
    return grp

def propose_transfers(df_inventory, transfer_cost_per_km_per_unit=0.01, max_transfer_fraction=0.5):
    """
    Propose transfers from surplus warehouses to deficit warehouses for each product category.
    transfer_cost_per_km_per_unit: cost INR per km per unit moved (simple estimation)
    max_transfer_fraction: fraction of surplus units that can be offered for transfer
    """
    inv = compute_surplus_deficit(df_inventory)
    inv = assign_coords(inv.rename(columns={'Warehouse_ID':'Warehouse_ID'}))
    proposals = []
    # for each product category handle separately
    cats = inv['Product_Category'].unique()
    for cat in cats:
        sub = inv[inv['Product_Category']==cat].copy()
        surplus = sub[sub['Delta']>0].sort_values('Delta', ascending=False)
        deficit = sub[sub['Delta']<0].sort_values('Delta')
        # iterate deficits and fill from largest surplus by cheapest distance*cost
        for di, drow in deficit.iterrows():
            need = -int(drow['Delta'])
            if need<=0: continue
            # compute distances to surplus warehouses
            surplus = surplus.copy()
            if surplus.empty: break
            surplus['dist_km'] = surplus.apply(lambda r: haversine(r['Lat'], r['Lon'], drow['Lat'], drow['Lon']), axis=1)
            surplus['available'] = (surplus['Delta'] * max_transfer_fraction).astype(int)
            surplus = surplus[surplus['available']>0]
            if surplus.empty: break
            surplus['unit_transfer_cost'] = surplus['dist_km'] * transfer_cost_per_km_per_unit
            # sort by unit_transfer_cost
            surplus = surplus.sort_values('unit_transfer_cost')
            for si, srow in surplus.iterrows():
                take = min(need, int(srow['available']))
                if take<=0: continue
                cost = take * srow['unit_transfer_cost']
                proposals.append({
                    'Product_Category': cat,
                    'From_Warehouse': srow['Warehouse_ID'],
                    'From_Location': srow['Location'],
                    'To_Warehouse': drow['Warehouse_ID'],
                    'To_Location': drow['Location'],
                    'Units_Transferred': take,
                    'Distance_km': round(srow['dist_km'],2),
                    'Estimated_Transfer_Cost_INR': round(cost,2),
                    'Storage_Cost_per_Unit_INR_from': srow['Storage_Cost_per_Unit'],
                    'Storage_Cost_per_Unit_INR_to': drow['Storage_Cost_per_Unit']
                })
                need -= take
                surplus.loc[si,'available'] -= take
                if need<=0:
                    break
    proposals_df = pd.DataFrame(proposals)
    return proposals_df
