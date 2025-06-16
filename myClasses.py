# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:59:28 2025

@author: BrunoFantoli
"""

"Imports"
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # Permet de générer des graphiques

radiation_data = pd.read_excel("Data/Solar radiation.xlsx", index_col=0)
data_hourly_T_out_degC = pd.read_excel("Data/T_ext.xlsx", index_col=0)
data_per_usage = pd.read_excel("Data/data_per_usage.xlsx", index_col=0)
elec_data = pd.read_excel("Data/elec_time_series.xlsx", index_col=0)

couleursperso = ['#003f38', '#deeaf8', '#f1efa3', '#d9d9d9']


"Classes"
class heating_unit:
    """ Classe qui représente un générateur de chaleur pour le chauffage ou l'ECS."""
    def __init__(self, heater_type, heating_power_kw, fuel, efficiency=0.9, purpose="heating", name=""):
        self.heater_type = heater_type
        self.heating_power_kw = heating_power_kw
        self.fuel = fuel
        self.efficiency = efficiency
        self.purpose = purpose
        self.name = name
        
    def show(self):
        print("La %s %s a une puissance nominale de %s kW."%(self.heater_type, self.name, self.heating_power_kw))

class hot_water_tank:
    """ Classe qui représente un ballon d'eau chaude."""
    def __init__(self, volume_l, name=None):
        self.volume_l = volume_l
        self.name = name
        
class pv_installation:
    """ Classe qui représente une installation photovoltaique."""
    def __init__(self, peak_power_kw, annual_production_kwh=0, location="Uccle"):
        self.peak_power_kw = peak_power_kw
        self.location = location
        if annual_production_kwh == 0:
            self.annual_production_kwh = peak_power_kw*1186.64 #1186.64 is the yearly production in kwh per kw peak installed of a fixed PV panel with optimized slope and orientation in Brussels according to PVGIS
        else:
            self.annual_production_kwh = annual_production_kwh
        self._distribute_production()
        
    def _distribute_production(self):
        scaler = self.annual_production_kwh/radiation_data[self.location].sum()
        self.hourly_production_kwh = radiation_data[self.location]*scaler
        
class building():
    """ Classe permettant de simuler le comportement d'un bâtiment.\n\n
    Parameters : \n\n
    name                            : The name of the building\n
    surface_area_m2                 : The heated floor area\n
    profile                         : The building's consumption profile, to be chosen from: "Manufacturing processes", "Trades (non-food)", "Trades (food)", "Education", "Office", "Crop farming and transportation", "Livestock farming", "Water supply and telecom", "Restaurants", "Food industry", "Wine industry", "Energy supply and rental", "Hotels", "Bakery", "Property management companies", "Hospital", "Recreational and social activities", "Construction-related activities"\n
    location                        : The city where the building is located\n
    annual_heat_consumption_kwh     : The building's annual heat consumption, in kWh\n
    share_shw_demand                : The share of this consumption used for domestic hot water (DHW)\n
    annual_elec_consumption_kwh     : The building's annual electricity consumption, in kWh\n
    share_ac                        : The share of this consumption that is alternating current\n
    co2_cost                        : The cost of emissions paid by the company if applicable, in €/ton\n
    v50                             : The air leakage rate per unit of envelope surface at 50 Pa, in m³/h/m³\n
    ventilation_setting             : Ventilation setting, to be chosen from: "No ventilation", "Demand management, central", "Demand management, local", "Time setting", "No or unknown setting", "Manual"\n
    vent_recovery_efficiency        : Efficiency of the heat recovery system in the ventilation\n
    opening_time                    : The building's opening time\n
    closing_time                    : The building's closing time\n
    opening_days_per_week           : Number of days the building is open per week\n
    type_ventilation                : Type of ventilation, to be chosen from: "No ventilation", "Supply", "Exhaust", "Supply and Exhaust"\n
    room_height_m                   : Average ceiling height in the building, in meters\n
    Q_vent_m3_h                     : Ventilation flow rate, in m³/h\n
    average_occupation              : The building's average occupancy\n
"""

    def __init__(self, name, surface_area_m2, profile="Office", location="Uccle", annual_heat_consumption_kwh=0, share_shw_demand=0, annual_elec_consumption_kwh=0, share_ac=0, co2_cost=0, Temp_in_comfort=24, Temp_in_reduced = 16, v50=6, ventilation_setting="No setting", vent_recovery_efficiency=0, opening_time=7, closing_time=18, opening_days_per_week=5, type_ventilation="No ventilation", room_height_m=2.8, Q_vent_m3_h=0, average_occupation=0, elec_price_peak_euro_per_kwh=0.17, elec_price_off_peak_euro_per_kwh=0.14, peak_start_time=7, peak_end_time=22, injection_price_euro_per_kwh=0.06, fuel_price_euro_per_kwh=0.04, annual_shw_consumption_l=-1, Temp_shw_degC=60, carbon_intensity_fuel_kg_per_kwh=0.218, carbon_intensity_grid_kg_per_kwh=0.216):
        self.name = name
        self.surface_area_m2 = surface_area_m2
        self.profile = profile
        self.custom_profile = None
        self.location = location # à choisir entre Uccle,	Gembloux,	Ovifat,	Diepenbeek,	Antwerp,	Dessel,	Sint-Katelijne-Waver,	Gijzenzele,	Beitem	, Zeebrugge
        self.annual_heat_consumption_kwh = annual_heat_consumption_kwh
        self.share_shw_demand = share_shw_demand
        self.share_ac = share_ac
        self.co2_cost = co2_cost
        self.Temp_in_comfort = Temp_in_comfort
        self.Temp_in_reduced = Temp_in_reduced
        self.v50 = v50
        self.ventilation_setting = ventilation_setting
        self.vent_recovery_efficiency = vent_recovery_efficiency
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.opening_days_per_week = opening_days_per_week
        self.type_ventilation = type_ventilation
        self.room_height = room_height_m
        self.Q_vent_m3_h = Q_vent_m3_h
        self.elec_price_peak_euro_per_kwh = elec_price_peak_euro_per_kwh
        self.elec_price_off_peak_euro_per_kwh = elec_price_off_peak_euro_per_kwh
        self.peak_start_time = peak_start_time
        self.peak_end_time = peak_end_time
        self.injection_price_euro_per_kwh = injection_price_euro_per_kwh
        self.Temp_shw_degC = Temp_shw_degC
        self.fuel_price_euro_per_kwh = fuel_price_euro_per_kwh
        self.carbon_intensity_fuel_kg_per_kwh = carbon_intensity_fuel_kg_per_kwh
        self.carbon_intensity_grid_kg_per_kwh = carbon_intensity_grid_kg_per_kwh
        self.fuel_indicator = 1
        
        self.protected_volume = surface_area_m2 * room_height_m
        self.heating_units = []
        self.total_heating_power_kw = 0
        self.hot_water_tanks = []
        self.pv_installations = []
        self.roofs = pd.DataFrame({'Surface': [],'Valeur U': [], 'Coefficient Ht': []})
        self.walls = pd.DataFrame({'Surface': [],'Valeur U': [], 'Coefficient Ht': []})
        self.floors = pd.DataFrame({'Surface': [],'Valeur U': [], 'Coefficient Ht': []})
        self.windows = pd.DataFrame({'Surface': [],'Valeur U': [], 'Coefficient Ht': [], 'Facteur solaire' : []})
        self.envelope = pd.DataFrame({'Surface': [],'Valeur U': [], 'Coefficient Ht': []})
        self.estimations = pd.DataFrame({'Déperditions chaleur transmission': [0],'Déperditions chaleur ventilation': [0], 'Déperditions chaleur in/exfiltration': [0]})
        self.hourly_pv_production_kwh = np.zeros(8760)
        if annual_elec_consumption_kwh==0:
            self.annual_elec_consumption_kwh = 140*self.surface_area_m2
        else:
            self.annual_elec_consumption_kwh = annual_elec_consumption_kwh
        
        if average_occupation==0:
            self.average_occupation = data_per_usage.loc["occupation par m2"][self.profile]*self.surface_area_m2
        else:
            self.average_occupation= average_occupation
            
        if annual_shw_consumption_l == -1:
            self.annual_shw_consumption_l = self.opening_days_per_week*52*self.average_occupation*data_per_usage.loc["ECS par personne par jour [l]"][self.profile]
        else:
            self.annual_shw_consumption_l = annual_shw_consumption_l
        
        
    def _show(self):
        print("La surface totale du bâtiment %s est de %s m². \nC'est un bâtiment de type %s qui se situe à %s. \n\nSa consommation annuelle de chauffage est de %s kWh et de %s kWh pour l'eau chaude sanitaire.\n\nSa consommation annuelle d'électricité est de %s kWh."%(self.name, self.surface_area_m2, self.profile, self.location, self.annual_heat_consumption_kwh, self.annual_heat_consumption_kwh*self.share_shw_demand/100,self.annual_elec_consumption_kwh))
    
    def _distribute_elec_cost(self):
        peak_hours = (self.hourly_grid_demand_kwh.index.hour >= self.peak_start_time) & (self.hourly_grid_demand_kwh.index.hour < self.peak_end_time) # type: ignore
        if(self.pv_installations==[]):
            self.hourly_elec_cost_euro = np.where(
                peak_hours,  # Check if it's peak hours
                self.hourly_grid_demand_kwh * self.elec_price_peak_euro_per_kwh, 
                self.hourly_grid_demand_kwh * self.elec_price_off_peak_euro_per_kwh
                )
        else:
            self.hourly_elec_cost_euro = np.where(
                self.hourly_grid_demand_kwh >= 0,  # If drawing power from the grid
                np.where(peak_hours,  # Check if it's peak hours
                         self.hourly_grid_demand_kwh * self.elec_price_peak_euro_per_kwh, 
                         self.hourly_grid_demand_kwh * self.elec_price_off_peak_euro_per_kwh),
                self.hourly_grid_demand_kwh * self.injection_price_euro_per_kwh  # Selling back to the grid
            )
    
    def _distribute_elec_demand(self):
        if self.custom_profile is None:
            self.hourly_elec_demand_kwh = elec_data[self.profile]
        else:
            # Charger les timestamps depuis elec_time_series.xlsx (à faire une seule fois, de préférence)
            time_index = elec_data.index
            # Créer une Series avec l’index temporel correct
            self.hourly_elec_demand_kwh = pd.Series(self.custom_profile, index=time_index)
            self.annual_elec_consumption_kwh = sum(self.hourly_elec_demand_kwh)
            
        self.hourly_elec_demand_kwh = self.hourly_elec_demand_kwh * self.annual_elec_consumption_kwh/sum(self.hourly_elec_demand_kwh)
        self.hourly_grid_demand_kwh = self.hourly_elec_demand_kwh - self.hourly_pv_production_kwh
        
        self._distribute_elec_cost()

    def _add_heating_unit(self, unit:heating_unit):
        """Ajouter un générateur de chaleur au bâtiment. \n \n
        Attention, le parametre doit être de type heating_unit."""
        self.heating_units.append(unit)
        self.total_heating_power_kw += unit.heating_power_kw
        
        if "elec" in unit.fuel or "élec" in unit.fuel or "Elec" in unit.fuel or "Élec" in unit.fuel:
            self.fuel_indicator = 0
        
    def _add_hot_water_tank(self,tank:hot_water_tank):
        """Ajouter un ballon d'eau chaude au bâtiment. \n \n
        Attention, le parametre doit être de type hot_water_tank."""
        self.hot_water_tanks.append(tank)
        
    def _add_pv_installation(self, pv_installation:pv_installation):
        """Ajouter une installation PV. \n \n
        Attention, le parametre doit être de type pv_installation."""
        self.pv_installations.append(pv_installation)
        if pv_installation.peak_power_kw > sum(self.roofs["Surface"]):
            print("L'installation PV est plus grande que le toit du bâtiment") # en considérant une puissance de 1 kW/m2
        self.hourly_pv_production_kwh = pv_installation.hourly_production_kwh
        self.hourly_grid_demand_kwh = self.hourly_elec_demand_kwh - self.hourly_pv_production_kwh

        self._distribute_elec_cost()

    def _add_roof(self,surface, U_value, tilt=0):
        self.roofs.loc[len(self.roofs)]=[surface, U_value, surface*U_value]

    def _add_wall(self,surface, U_value):
        self.walls.loc[len(self.walls)]=[surface, U_value, surface*U_value]
        
    def _add_floor(self,surface, U_value):
        self.floors.loc[len(self.floors)]=[surface, U_value, surface*U_value]
        
    def _add_window(self,surface, U_value, solar_factor=0.7):
        self.windows.loc[len(self.windows)]=[surface, U_value, surface*U_value, solar_factor]
        
    def _show_envelope(self):
        labels = "Roofs", "Floors", "Walls", "Windows"
        title = "Distribution of the transmission losses through the envelope"
        fig, ax = plt.subplots(figsize=(3,3))
        sizes = [sum(self.roofs["Coefficient Ht"]), sum(self.floors["Coefficient Ht"]), sum(self.walls["Coefficient Ht"]), sum(self.windows["Coefficient Ht"])]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=couleursperso)
        plt.title(title)
        plt.show()
        return fig
        
    def _update_estimations(self):
        # Transmission
        T_ext_moyenne = 6 #°C
        H_tot = sum(self.roofs["Coefficient Ht"]) + sum(self.floors["Coefficient Ht"]) + sum(self.walls["Coefficient Ht"]) + sum(self.windows["Coefficient Ht"])
        self.estimations['Déperditions chaleur transmission'] = 0.34*H_tot*(self.Temp_in_comfort-T_ext_moyenne)*5800/1000
        
        # In_exfiltration
        total_loss_surface = sum(self.roofs["Surface"]) + sum(self.walls["Surface"]) + sum(self.windows["Surface"])
        self.estimations['Déperditions chaleur in/exfiltration'] = 0.34*0.04*self.v50*total_loss_surface*(self.Temp_in_comfort-T_ext_moyenne)*5800/1000
        
        # Ventilation
        if self.ventilation_setting == "Demand management, central":
            f_reduc_vent = 0.8
        else :
            if self.ventilation_setting == "Demand management, local":
                f_reduc_vent = 0.7
            else:
                f_reduc_vent = 1
        
        if "Demand management" in self.ventilation_setting or self.ventilation_setting== "Time setting":
            f_load = (self.closing_time-self.opening_time)/24 * self.opening_days_per_week/7
        else:
            f_load = 1
        
        if self.type_ventilation == "No ventilation":
            self.Q_vent_m3_h = 0.04*self.protected_volume
        else:
            if self.Q_vent_m3_h == 0: # type: ignore
                self.Q_vent_m3_h = 22*self.average_occupation
        
        f_preheat = 1 - (0.71*self.vent_recovery_efficiency)
        self.estimations['Déperditions chaleur ventilation'] = 0.34*self.Q_vent_m3_h*f_reduc_vent*f_preheat*f_load*(self.Temp_in_comfort-T_ext_moyenne)*5800/1000
        
    def _show_estimations(self):
        self._update_estimations()
        labels = "Transmission", "Ventilation", "in-/ex-filtration"
        title = "Distribution of all heat losses through the envelope"
        fig, ax = plt.subplots(figsize=(3,3))
        sizes = self.estimations.loc[0,:]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=couleursperso)
        plt.title(title)
        plt.show()
        return fig
        
    def _set_consumptions(self,annual_elec_consumption_kwh=-1, annual_heat_consumption_kwh=-1):
        if annual_elec_consumption_kwh > -1 :
            self.annual_elec_consumption_kwh = annual_elec_consumption_kwh
        if annual_heat_consumption_kwh > -1 :
            self.annual_heat_consumption_kwh = annual_heat_consumption_kwh
            
    def _hourly_energy_balance(self):
        """Inside Temperature"""
        self.hourly_T_out_degC = data_hourly_T_out_degC[self.location]
        #defining hourly_T_in_degC
        T_ambiant = self.Temp_in_comfort # Example ambient temperature
        T_reduced = self.Temp_in_reduced  # Example reduced temperature
        start_hour = self.opening_time  # Start of ambient period
        end_hour = self.closing_time   # End of ambient period
        
        # Example: Load your existing timeseries (assuming it's already a pandas Series)
        # outside_temp = pd.read_csv("your_file.csv", parse_dates=["timestamp"], index_col="timestamp")
        
        # Create the inside temperature series
        self.hourly_T_in_degC = pd.Series(
            T_ambiant if ts.weekday() < self.opening_days_per_week and start_hour <= ts.hour < end_hour else T_reduced
            for ts in self.hourly_T_out_degC .index # type: ignore
        ) # type: ignore
        # Assign the same index
        self.hourly_T_in_degC.index = self.hourly_T_out_degC .index
        self.hourly_T_in_degC.name = "Inside Temperature"
        
        """Heat losses"""
        #Q_trans
        self.hourly_Q_trans_kwh = (self.hourly_T_in_degC-self.hourly_T_out_degC )*(sum(self.roofs["Coefficient Ht"])+sum(self.walls["Coefficient Ht"])+sum(self.windows["Coefficient Ht"])+sum(self.floors["Coefficient Ht"]))/1000
        #Q_in-ex
        total_loss_surface = sum(self.roofs["Surface"]) + sum(self.walls["Surface"]) + sum(self.windows["Surface"])
        self.hourly_Q_in_ex_kwh = (self.hourly_T_in_degC-self.hourly_T_out_degC )*0.34*0.04*self.v50*total_loss_surface/1000
        #Q_vent
        f_preheat = 1 - (0.71*self.vent_recovery_efficiency)
        self.hourly_Q_vent_kwh = pd.Series(
            0.34 * self.Q_vent_m3_h * f_preheat * (self.hourly_T_in_degC[ts] - self.hourly_T_out_degC [ts]) / 1000
            if ts.weekday() < self.opening_days_per_week and start_hour <= ts.hour < end_hour else 0
            for ts in self.hourly_T_out_degC .index # type: ignore
        ) # type: ignore

        # Assign the same index
        self.hourly_Q_vent_kwh.index = self.hourly_T_out_degC .index
        self.hourly_Q_vent_kwh.name = "Ventilation Losses (kWh)"    
        
        """Heat gains"""
        #Q_solar
        if sum(self.windows["Facteur solaire"])==0:
            solar_factor = 0
        else:
            solar_factor = np.average(self.windows["Facteur solaire"],weights=self.windows["Surface"])
        self.hourly_solar_gains_kwh = 0.6*sum(self.windows["Surface"])*solar_factor*radiation_data[self.location]/1000 # type: ignore
        
        """Energy balance"""
        hourly_energy_balance = self.hourly_Q_trans_kwh+self.hourly_Q_in_ex_kwh+self.hourly_Q_vent_kwh-self.hourly_solar_gains_kwh
        self.hourly_heating_demand_kwh = pd.Series(
            hourly_energy_balance[ts]
            if hourly_energy_balance[ts] > 0 else 0 # type: ignore
            for ts in self.hourly_T_out_degC .index # type: ignore
        ) # type: ignore
        self.hourly_heating_demand_kwh.index = self.hourly_T_out_degC .index
        self.hourly_heating_demand_kwh.name = "Heating Demand (kWh)" 
        self.hourly_cooling_demand_kwh = pd.Series(
            -hourly_energy_balance[ts]
            if hourly_energy_balance[ts] < 0 else 0 # type: ignore
            for ts in self.hourly_T_out_degC .index # type: ignore
        ) # type: ignore
        self.hourly_cooling_demand_kwh.index = self.hourly_T_out_degC .index
        self.hourly_cooling_demand_kwh.name = "Cooling Demand (kWh)" 
        
        """Sanitary Hot Water"""
        self.hourly_shw_demand_kwh = pd.Series(
            self.average_occupation*data_per_usage.loc["ECS par personne par jour [l]"][self.profile]/(end_hour-start_hour)*(self.Temp_shw_degC-10)*1.16/1000
            if ts.weekday() < self.opening_days_per_week and start_hour <= ts.hour < end_hour else 0
            for ts in self.hourly_T_out_degC .index # type: ignore
        ) # type: ignore
        self.hourly_shw_demand_kwh.index = self.hourly_T_out_degC .index
        self.hourly_shw_demand_kwh.name = "Sanitary Hot Water Demand (kWh)" 
        
        "Boiler requirements"
        self.hourly_boiler_consumption = pd.Series(
            (self.hourly_heating_demand_kwh[ts]+self.hourly_shw_demand_kwh[ts])/self.heating_units[0].efficiency
            if self.hourly_heating_demand_kwh[ts]+self.hourly_shw_demand_kwh[ts] < self.total_heating_power_kw else self.total_heating_power_kw/self.heating_units[0].efficiency # type: ignore
            for ts in self.hourly_T_out_degC.index # type: ignore
        ) # type: ignore
        self.hourly_boiler_consumption.index = self.hourly_T_out_degC .index
        self.hourly_boiler_consumption.name = "Boiler consumption (kWh)" 
        if(self.hourly_boiler_consumption == self.total_heating_power_kw).sum()>0:
            print("Potentiel problème d'inconfort pendant %s heures sur l'année."%((self.hourly_boiler_consumption == self.total_heating_power_kw).sum()))
        
        "If the boiler runs on electricity, its consumption must be added to the elec consumption"
        if self.fuel_indicator == 0:
            self.hourly_elec_demand_kwh += self.hourly_boiler_consumption
            self.hourly_grid_demand_kwh = self.hourly_elec_demand_kwh - self.hourly_pv_production_kwh
            self._distribute_elec_cost()
            self.fuel_price_euro_per_kwh = 0
                
        
    def _show_boiler_consumption(self, timestep='hourly'):
        fig, ax = plt.subplots(figsize=(5,5))
        if timestep == "monthly":
            monthly_consumption = self.hourly_boiler_consumption.resample("M").sum()
            plt.bar(monthly_consumption.index, monthly_consumption, color="tab:red", alpha=0.8)    
        if timestep == "weekly":
            smoothed = self.hourly_boiler_consumption.rolling(window=24*7).sum()
            plt.plot(smoothed, label="Consommation hebdomadaire", color=couleursperso[0])
        if timestep == "daily":
            smoothed = self.hourly_boiler_consumption.rolling(window=24).sum()
            plt.plot(smoothed, label="Consommation journalière", color=couleursperso[0])
        else:
            plt.plot(self.hourly_boiler_consumption, label="Fonctionnement de la chaudière", color=couleursperso[0], linewidth=1.5, alpha=0.8)

        plt.xlabel("Temps")  # Label for X-axis
        plt.ylabel("Consommation (kWh)")  # Label for Y-axis
        plt.title("Consommation annuelle de la chaudière")  # Add title
        plt.legend()  # Show legend
        plt.grid(True, linestyle="--", alpha=0.5)  # Add grid with transparency
        plt.show()
        
        result = ("La consommation annuelle totale du bâtiment {} est de {:.1f} MWh de combustible et de {:.1f} MWh d'électricité (dont {:.1f} MWh viennent du réseau. La production d'électrcitié renouvelable est de {:.1f} MWh. \n \nCela correspond à {:,.0f} € pour de combustible et {:,.0f} € d'électricité.\nOu encore {:.1f} tCO2 pour le combustible et {:.1f} tCO2 pour l'électricité.".format(
            self.name,
            self.hourly_boiler_consumption.sum()/1000,
            self.hourly_elec_demand_kwh.sum()/1000, 
            self.hourly_grid_demand_kwh.sum()/1000,
            self.hourly_pv_production_kwh.sum()/1000,
            self.hourly_boiler_consumption.sum()*self.fuel_price_euro_per_kwh,
            self.hourly_elec_cost_euro.sum(),
            self.hourly_boiler_consumption.sum()*self.carbon_intensity_fuel_kg_per_kwh/1000,
            self.hourly_grid_demand_kwh.sum()*self.carbon_intensity_grid_kg_per_kwh/1000
            ))
        return result
        
    def _compare_buildings(self,other_building):
        self._hourly_energy_balance()
        other_building._hourly_energy_balance()
        if(self.hourly_boiler_consumption.sum()*self.fuel_indicator < other_building.hourly_boiler_consumption.sum()*other_building.fuel_indicator):
            comparaison_combustible = "{:,.0f} MWh de combustible en moins".format(abs(other_building.fuel_indicator*other_building.hourly_boiler_consumption.sum()-self.fuel_indicator*self.hourly_boiler_consumption.sum())/1000)
        else: 
            if(self.hourly_boiler_consumption.sum()*self.fuel_indicator > other_building.hourly_boiler_consumption.sum()*other_building.fuel_indicator):
                comparaison_combustible = "{:,.0f} MWh de combustible en plus".format(abs(other_building.fuel_indicator*other_building.hourly_boiler_consumption.sum()-self.fuel_indicator*self.hourly_boiler_consumption.sum())/1000)
            else:
                comparaison_combustible = "la même quantité de combustible"
                
        if(self.hourly_elec_demand_kwh.sum()<other_building.hourly_elec_demand_kwh.sum()):
            comparaison_elec = "{:,.0f} MWh d'électricité en moins".format(abs(other_building.hourly_elec_demand_kwh.sum()-self.hourly_elec_demand_kwh.sum())/1000)
        else: 
            if(self.hourly_elec_demand_kwh.sum()>other_building.hourly_elec_demand_kwh.sum()):
                comparaison_elec = "{:,.0f} MWh d'électricité en plus".format(abs(other_building.hourly_elec_demand_kwh.sum()-self.hourly_elec_demand_kwh.sum())/1000)
            else:
                comparaison_elec = "la même quantité d'électricité"
                
        if(self.hourly_pv_production_kwh.sum() > other_building.hourly_pv_production_kwh.sum()):
            comparaison_enr = "{:,.0f} MWh d'électricité renouvelable en plus".format(abs(self.hourly_pv_production_kwh.sum()-other_building.hourly_pv_production_kwh.sum())/1000)
        else: 
            if(self.hourly_pv_production_kwh.sum() < other_building.hourly_pv_production_kwh.sum()):
                comparaison_enr = "{:,.0f} MWh d'électricité renouvelable en moins".format(abs(self.hourly_pv_production_kwh.sum()-other_building.hourly_pv_production_kwh.sum())/1000)
            else:
                comparaison_enr = "la même quantité d'énergie renouvelable"


        result = ("Par rapport au bâtiment {}, le bâtiment {} consomme {} et {}.\nIl produit {}. \n\nL'économie est donc de {:,.0f}€ par an et de {:,.1f} tCO2 par an.".format(
            other_building.name,
            self.name,
            comparaison_combustible,
            comparaison_elec,
            comparaison_enr,
            (other_building.hourly_boiler_consumption.sum()*other_building.fuel_price_euro_per_kwh*other_building.fuel_indicator + other_building.hourly_elec_cost_euro.sum()) - (self.hourly_boiler_consumption.sum()*self.fuel_price_euro_per_kwh*self.fuel_indicator + self.hourly_elec_cost_euro.sum()),
            ((other_building.hourly_boiler_consumption.sum()*other_building.carbon_intensity_fuel_kg_per_kwh*other_building.fuel_indicator + other_building.hourly_grid_demand_kwh.sum()*other_building.carbon_intensity_grid_kg_per_kwh) - (self.hourly_boiler_consumption.sum()*self.carbon_intensity_fuel_kg_per_kwh*self.fuel_indicator + self.hourly_grid_demand_kwh.sum()*self.carbon_intensity_grid_kg_per_kwh))/1000
            ))
        return result
        
