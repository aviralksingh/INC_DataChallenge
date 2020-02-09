import pandas as pd
import re
import numpy as np
import os
import sys
import logging

import matplotlib.pyplot as plt

sys.path.append("./")
sys.path.append("./../")
class INC5000():
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.prefix = "Data/inc5000_all10years.csv"
        self.logger.info("*****************************")
        self.logger.info("*   Initializing INC 5000   *")
        self.logger.info("*****************************")
        self.df = pd.read_csv(self.prefix,encoding= 'unicode_escape')
        self.df.columns = self.df.columns.str.replace('\_ - ','',regex=True)
        self.num_rows= len(self.df.index)
        self.num_columns = len(self.df.columns)
        self.index,self.columns,self.values,self.dtypes=self.get_dataframe_properties()
        self.DEBUG_display_df_properties()
        self.logger.info("*****************************")
        self.logger.info("*   Extracting Unique Index *")
        self.logger.info("*****************************")
        self.Years=self.get_unique_index(str(self.columns[0]))
        self.Cities = self.get_unique_index(str(self.columns[2]))
        self.Companies = self.get_unique_index(str(self.columns[5]))
        self.States = self.get_unique_index(str(self.columns[6]))
        self.StatesName = self.get_unique_index(str(self.columns[7]))
        self.Industries = self.get_unique_index(str(self.columns[-2]))
        self.Metros = self.get_unique_index(str(self.columns[-1]))
        self.DEBUG_display_unique_labels()
        self.logger.info("*****Extraction Complete*****")

        self.plotCityGrowth()

    def get_dataframe_properties(self):
        return self.df.index,self.df.columns,self.df.values,self.df.dtypes

    def get_unique_index(self,column_name):
        return self.df[column_name].unique()

    def plotCityGrowth(self):
        states=[]
        state_revenue=[]
        state_years=[]
        state_cum_revenue=[]
        Revenue_df=self.df.loc[:,['year','revenue','state_s']]
        for state in self.States:
            Revenue=[]
            years = []
            Cumulative_Revenue=[]
            for year in self.Years:
                Revenue.append(np.sum(Revenue_df.revenue[(Revenue_df.year == year) & (Revenue_df.state_s == state)]))
                years.append(year)
            Sorted_Revenue = [x for _, x in sorted(zip(years, Revenue))]
            series=series = pd.Series(Sorted_Revenue)
            Cumulative_Revenue = series.cumsum()
            years.sort()
            state_years.append(years)
            states.append(state)
            state_revenue.append(Sorted_Revenue)
            state_cum_revenue.append(Cumulative_Revenue)
        self.logger.info(f'city : {state_revenue}')
        self.logger.info(f'city : {states}')
        self.logger.info(f'city : {years}')

        print(len(state_revenue[0]))

        plt.xlabel("X-axis")
        plt.ylabel("Revenue")
        plt.title("A test graph")
        # for revenue in state_revenue:
        plt.bar(years, state_revenue[0])


        yplot=np.vstack((state_cum_revenue[0],state_cum_revenue[1]))
        yplot=np.vstack((yplot,state_cum_revenue[2]))

        #
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.stackplot(years, state_cum_revenue, labels=['CA','MA','IN'])
        ax.set_title('Cumulative Revenue over time')
        ax.legend(loc='upper left')
        ax.set_ylabel('Cumulative Revenue')
        fig.tight_layout()
        plt.show()
        plt.legend()

    def analyzecitydataframe(self):
        self.logger.info("*****************************")
        self.logger.info("*   Setting Cities as Index *")
        self.logger.info("*****************************")
        self.df.set_index(str(self.columns[2]), inplace=True)
        self.logger.info(f'Values : {self.df.index}')
        Cities= self.df.loc(['Los Angeles'])
        self.logger.info(f'Values : {self.df.head()}')

    def DEBUG_display_df_properties(self):
        self.logger.debug("*****************************")
        self.logger.debug("*Debug DataFrame Properties *")
        self.logger.debug("*****************************")
        self.logger.debug(f'Titles : {self.columns}')
        self.logger.debug(f'Titles type: {type(self.columns)}')
        self.logger.debug(f'Index : {self.index}')
        self.logger.debug(f'Index type : {type(self.index)}')
        self.logger.debug(f'DataTypes : {self.dtypes}')
        self.logger.debug("*****************************")


    def DEBUG_display_unique_labels(self):
        self.logger.debug("*****************************")
        self.logger.debug("*   Debug Unique Properties *")
        self.logger.debug("*****************************")
        self.logger.debug(f'Years : {self.Years}')
        self.logger.debug(f'Cities : {self.Cities}')
        self.logger.debug(f'Companies : {self.Companies}')
        self.logger.debug(f'States : {self.States}')
        self.logger.debug(f'States : {self.StatesName}')
        self.logger.debug(f'Industries : {self.Industries}')
        self.logger.debug(f'Metros : {self.Industries}')
        self.logger.debug("*****************************")

if __name__=="__main__":
    data= INC5000()
