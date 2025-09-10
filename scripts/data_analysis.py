import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import os

# Create folders if they don’t exist
os.makedirs("results/visualizations", exist_ok=True)

# Set style for plots
plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")


# Load the data

def load_data(file_path):
    return pd.read_csv(file_path)

data = load_data(r"C:\Users\rawal\OneDrive\Desktop\Marketing Campaign Effectiveness Analysis\Market Campaign Effective Analysis.csv")
print(data.head())


# Data preprocessing
def preprocess_data(df):
    # Create a copy to avoid modifying the original
    df_clean = df.copy()
    
    # Handle missing values in Income (replace with median)
    df_clean['Income'] = df_clean['Income'].fillna(df_clean['Income'].median())
    
    # Calculate age from Year_Birth
    df_clean['Age'] = 2023 - df_clean['Year_Birth']
    
    # Calculate total spending
    df_clean['Total_Spending'] = df_clean['MntWines'] + df_clean['MntFruits'] + \
                                df_clean['MntMeatProducts'] + df_clean['MntFishProducts'] + \
                                df_clean['MntSweetProducts'] + df_clean['MntGoldProds']
    
    # Calculate total purchases
    df_clean['Total_Purchases'] = df_clean['NumWebPurchases'] + df_clean['NumCatalogPurchases'] + \
                                 df_clean['NumStorePurchases'] + df_clean['NumDealsPurchases']
    
    # Calculate total children
    df_clean['Total_Children'] = df_clean['Kidhome'] + df_clean['Teenhome']
    
    # Calculate customer tenure (days since enrollment)
    df_clean['Dt_Customer'] = pd.to_datetime(df_clean['Dt_Customer'])
    df_clean['Tenure_Days'] = (pd.to_datetime('2023-01-01') - df_clean['Dt_Customer']).dt.days
    
    return df_clean

# Generate visualizations


def create_visualizations(df):
    # 1. Response rate by education
    df['Response'].groupby(df['Education']).mean().plot(kind='bar')
    plt.title("Response Rate by Education")
    plt.xlabel("Education")
    plt.ylabel("Response Rate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("results/visualizations/response_by_education.png")
    plt.close()

    # 2. Response rate by marital status
    df['Response'].groupby(df['Marital_Status']).mean().plot(kind='bar')
    plt.title("Response Rate by Marital Status")
    plt.xlabel("Marital Status")
    plt.ylabel("Response Rate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("results/visualizations/response_by_marital_status.png")
    plt.close()
    
    # 3. Income distribution by response
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Response', y='Income', data=df)
    plt.title('Income Distribution by Response')
    plt.xlabel('Response (0=No, 1=Yes)')
    plt.ylabel('Income')
    plt.tight_layout()
    plt.savefig('results/visualizations/income_by_response.png')
    plt.close()
    
    # 4. Spending patterns by response
    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                    'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    
    responder_spending = df[df['Response'] == 1][spending_cols].mean()
    non_responder_spending = df[df['Response'] == 0][spending_cols].mean()
    
    plt.figure(figsize=(12, 6))
    x = np.arange(len(spending_cols))
    width = 0.35
    
    plt.bar(x - width/2, responder_spending, width, label='Responders')
    plt.bar(x + width/2, non_responder_spending, width, label='Non-Responders')
    
    plt.xlabel('Product Category')
    plt.ylabel('Average Spending')
    plt.title('Spending Patterns by Response')
    plt.xticks(x, [col.replace('Mnt', '') for col in spending_cols], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/visualizations/spending_by_response.png')
    plt.close()
    
    # 5. Channel preference by response
    channel_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'NumDealsPurchases']
    
    responder_channels = df[df['Response'] == 1][channel_cols].mean()
    non_responder_channels = df[df['Response'] == 0][channel_cols].mean()
    
    plt.figure(figsize=(12, 6))
    x = np.arange(len(channel_cols))
    width = 0.35
    
    plt.bar(x - width/2, responder_channels, width, label='Responders')
    plt.bar(x + width/2, non_responder_channels, width, label='Non-Responders')
    
    plt.xlabel('Purchase Channel')
    plt.ylabel('Average Number of Purchases')
    plt.title('Channel Preferences by Response')
    plt.xticks(x, [col.replace('Num', '').replace('Purchases', '') for col in channel_cols], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/visualizations/channels_by_response.png')
    plt.close()
    
    # 6. Correlation heatmap
    plt.figure(figsize=(12, 10))
    numeric_cols = ['Income', 'Total_Spending', 'Total_Purchases', 'Total_Children', 
                   'Tenure_Days', 'Recency', 'Age', 'Response']
    
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('results/visualizations/correlation_heatmap.png')
    plt.close()


# Calculate key metrics
def calculate_metrics(df):
    metrics = {}
    
    # Overall response rate
    metrics['overall_response_rate'] = df['Response'].mean() * 100
    
    # Response rate by campaign
    campaigns = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']
    campaign_rates = {}
    
    for campaign in campaigns:
        campaign_rates[campaign] = df[campaign].mean() * 100
    
    metrics['campaign_rates'] = campaign_rates
    
    # Average spending by responders vs non-responders
    metrics['avg_spending_responders'] = df[df['Response'] == 1]['Total_Spending'].mean()
    metrics['avg_spending_non_responders'] = df[df['Response'] == 0]['Total_Spending'].mean()
    
    # Average income by response
    metrics['avg_income_responders'] = df[df['Response'] == 1]['Income'].mean()
    metrics['avg_income_non_responders'] = df[df['Response'] == 0]['Income'].mean()
    
    return metrics


# Main execution
if __name__ == "__main__":
    # Load and preprocess data
    df = load_data(r"C:\Users\rawal\OneDrive\Desktop\Marketing Campaign Effectiveness Analysis\Market Campaign Effective Analysis.csv")
    df_clean = preprocess_data(df)
    
    # Create visualizations
    create_visualizations(df_clean)
    
    # Calculate metrics
    metrics = calculate_metrics(df_clean)
    
    # Print key metrics
    print("Marketing Campaign Analysis Results")
    print("===================================")
    print(f"Overall Response Rate: {metrics['overall_response_rate']:.2f}%")
    print("\nResponse Rates by Campaign:")
    for campaign, rate in metrics['campaign_rates'].items():
        print(f"{campaign}: {rate:.2f}%")
    
    print(f"\nAverage Spending - Responders: ${metrics['avg_spending_responders']:.2f}")
    print(f"Average Spending - Non-Responders: ${metrics['avg_spending_non_responders']:.2f}")
    
    print(f"\nAverage Income - Responders: ${metrics['avg_income_responders']:.2f}")
    print(f"Average Income - Non-Responders: ${metrics['avg_income_non_responders']:.2f}")


