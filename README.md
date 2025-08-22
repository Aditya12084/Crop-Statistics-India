# Crop Statistics India 🌾📊

A data analysis and visualization project on Indian crop statistics.  
This project leverages Python, Pandas, Streamlit to analyze agricultural data and present insights interactively.  

---

## 📌 Features
- Cleaned and structured agricultural dataset for analysis.  
- Statistical summaries and trends of crop production in India.  
- Interactive visualizations with **Streamlit**.  
- Focus on identifying crop yields, production patterns, and seasonality.  
- Scalable for future Machine Learning-based crop prediction.

---

## 🗂️ Project Structure  

Crop-Statistics-India/  
│  
├── data/ # Raw and cleaned datasets  
├── cleaned_dataset.ipynb  
├── app.py  
├── requirements.txt # Project dependencies  
├── README.md # Project description  

## 📄 Dataset Column Descriptions

| Column Name | Description |
|-------------|-------------|
| **state** | Name of the state or union territory in India where the crop is grown. |
| **district** | Name of the district within the state where the crop cultivation took place. |
| **crop** | The name of the agricultural crop being recorded (e.g., Rice, Wheat, Cotton). |
| **year** | The year in which the crop was cultivated or harvested. |
| **season** | The agricultural season of cultivation (e.g., Kharif, Rabi, Summer, Whole Year, Autumn, Winter). |
| **area** | Total cultivated land area for the crop in **hectares**. |
| **production** | Total production output of the crop in **tonnes**. |
| **yield** | Crop yield per unit area, usually calculated as *Production ÷ Area* (tonnes per hectare). |

## 📊 Example Visualizations

This project provides multiple interactive visualizations to explore crop production and yield trends across India:

- 📈 Line Charts – Showing crop production trends over the years
- 📊 Bar Charts – Comparing crop yields across different states
- 🔗 Correlation Matrix – Understanding relationships between various crops and production factors
- 🟢 Bubble Charts – Representing multi-dimensional crop statistics with size and color encoding
- 🌡 Heatmaps – Highlighting variations in crop vs season production

---

⚡ Made with ❤️ using Streamlit
