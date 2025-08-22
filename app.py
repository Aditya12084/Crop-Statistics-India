import pandas as pd
import streamlit as st
import plotly.express as px

def show_metrics(df, title="India"):
    total_production = df["production"].sum()
    total_area = df["area"].sum()
    avg_yield = df["yield"].mean()
    num_crops = df["crop"].nunique()
    num_states = df["state"].nunique()
    num_years = df["year"].nunique()

    st.header(f"Key Metrics - {title}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌾 Total Production (tons)", f"{total_production:,.0f}")
    with col2:
        st.metric("📏 Total Area (hectares)", f"{total_area:,.0f}")
    with col3:
        st.metric("⚖️ Average Yield (t/ha)", f"{avg_yield:.2f}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("🪴 Number of Crops", num_crops)
    with col5:
        st.metric("🗺️ States Covered", num_states)
    with col6:
        st.metric("📅 Years Covered", num_years)


# Streamlit page config
st.set_page_config(layout='wide', page_title='Crop Production Dashboard')
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem; /* Reduce default padding */
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Crop Production Statistics in India")
st.sidebar.title("Customize Your View")

# Load dataset
df = pd.read_csv("data/main_crops.csv")

# Sidebar selector
state_option = st.sidebar.selectbox(
    "Select Region",
    options=["All India"] + sorted(df["state"].unique())
)

# ---------------- STATE LEVEL VIEW ----------------
if state_option != "All India":

    # Filter for selected state
    filtered_df = df[df["state"] == state_option]
    show_metrics(filtered_df, title=state_option)

    # ---- Crop-wise Production ----
    crop_prod = filtered_df.groupby("crop")["production"].sum().reset_index()
    fig1 = px.bar(crop_prod, x="crop", y="production", title=f"🌾 Crop-wise Production in {state_option}")
    st.plotly_chart(fig1, use_container_width=True)

    # ---- Yield Trend ----
    yield_trend = filtered_df.groupby("year")["yield"].mean().reset_index()
    fig2 = px.line(yield_trend, x="year", y="yield", markers=True,
                   title=f"📈 Yield Trend in {state_option}")
    st.plotly_chart(fig2, use_container_width=True)

    # ---- Heatmap: Crop vs Season ----
    heatmap_df = filtered_df.groupby(["crop", "season"])["production"].sum().reset_index()
    fig3 = px.density_heatmap(
        heatmap_df,
        x="season",
        y="crop",
        z="production",
        title=f"🔥 Crop vs Season Production in {state_option}",
        color_continuous_scale="Turbo"
    )
    fig3.update_layout(
        width=1000,
        height=700,
        xaxis_title="Season",
        yaxis_title="Crop",
        title_x=0.3,
        font=dict(size=14)
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ---------------- SEASON ANALYSIS ----------------
    st.subheader("🌾 Season Analysis")

    # Markdown table
    st.markdown("""
    | Season       | Time Period                | Characteristics |
    |--------------|----------------------------|-----------------|
    | **Kharif**   | **June - October** (monsoon season) | Sown at the beginning of the rainy season, harvested at the end; require a lot of water. |
    | **Rabi**     | **November - April** (winter season) | Sown after the monsoon, harvested in spring; require cooler climate and less water. |
    | **Summer**   | **March - June** (pre-monsoon) | Grown between Rabi harvest and Kharif sowing; often need irrigation. |
    | **Whole Year** | **Any time** | Can be grown throughout the year due to suitable climate or controlled environments. |
    | **Autumn**   | **September - November** | Transitional season after Kharif harvest, before Rabi sowing; short-duration crops. |
    | **Winter**   | **December - February** | Cold-season crops; sometimes grown entirely within the coldest months. |
    """)

    seasons = filtered_df["season"].unique()
    selected_season = st.selectbox("Select Season:", seasons)

    year_range = st.slider(
        "Select Year Range:",
        int(df["year"].min()), int(df["year"].max()),
        (int(df["year"].min()), int(df["year"].max()))
    )

    # Apply BOTH filters (state + season + year)
    filtered_df_season_year = filtered_df[
        (filtered_df["season"] == selected_season) &
        (filtered_df["year"].between(year_range[0], year_range[1]))
    ]

    # Layout for charts
    col1, col2 = st.columns(2)

    with col1:
        # Apply year filter for all seasons of the state
        year_filtered_df = filtered_df[
            (filtered_df["year"].between(year_range[0], year_range[1]))
        ]
        total_production = year_filtered_df["production"].sum()

        if total_production > 0:
            seasonal_share = (
                year_filtered_df.groupby("season")["production"].sum().reset_index()
            )
            seasonal_share["share"] = seasonal_share["production"] / total_production * 100

            fig_season_share = px.pie(
                seasonal_share,
                values="share",
                names="season",
                title=f"🍰 Seasonal Share of Production in {state_option}"
            )
            st.plotly_chart(fig_season_share, use_container_width=True)
        else:
            st.warning("No data available for selected range.")

    with col2:
        if not filtered_df_season_year.empty:
            top_crops = (
                filtered_df_season_year.groupby("crop")["production"].sum()
                .reset_index()
                .sort_values(by="production", ascending=False)
                .head(5)
            )
            fig_top_crops = px.bar(
                top_crops,
                x="crop",
                y="production",
                title=f"Top Crops in {selected_season}",
                text="production"
            )
            st.plotly_chart(fig_top_crops, use_container_width=True)
        else:
            st.warning("No crop data for this season and year range.")

    coconut_df = pd.read_csv("data/coconut_filtered.csv")

    selected_state=state_option

    state_df = coconut_df[coconut_df['state'] == selected_state]

    st.header("Coconut Crop Analysis")
    if state_df.empty:
        st.warning("⚠️ No data available after filtering.")
    else:

        prod_trend = state_df.groupby("year")["production"].sum().reset_index()

        fig1 = px.line(
            prod_trend,
            x="year",
            y="production",
            title=f"Coconut Production Over Years in {selected_state}"
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Area vs Production
        if "area" in state_df.columns and "production" in state_df.columns:
            fig2 = px.scatter(state_df, x="area", y="production", size="production", color="year",
                              title=f"Area vs Production in {selected_state}")
            st.plotly_chart(fig2, use_container_width=True)

        # Average yield per year
        if "year" in state_df.columns and "yield" in state_df.columns:
            avg_yield = state_df.groupby("year")["yield"].mean().reset_index()
            fig3 = px.line(avg_yield, x="year", y="yield", title=f"Average Yield Over Years in {selected_state}")
            st.plotly_chart(fig3, use_container_width=True)


        # Group by district and sum production
        district_prod = state_df.groupby("district")["production"].sum().reset_index()

        # Sort and take top 10 districts
        top_districts = district_prod.sort_values(by="production", ascending=False).head(10)

        # Plotly bar chart
        fig = px.bar(
            top_districts,
            x="district",
            y="production",
            color="production",
            text="production",
            title=f"Top 10 Districts by Coconut Production in {selected_state}",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            xaxis_title="District",
            yaxis_title="Production",
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------- NATIONAL VIEW ----------------
else:
    st.markdown("""
        🌾 **Agriculture Data Analysis (India)**  

        Analyze and visualize India's crop production trends across states, districts, and years.  
        This project explores agricultural patterns using a cleaned dataset from **Kaggle**  
        Crop Production Dataset – 1997 to 2020
        originally sourced from the [Government of India – Directorate of Economics and Statistics](https://data.gov.in)    

        🛠️ **Tech Stack:** Python (Pandas, Plotly, Streamlit)  
        📊 **Features:** 
        - Yearly crop yield & production trends  
        - State-wise & district-wise comparisons  
        - Seasonal insights across major crops  
        - Interactive visualizations for exploration  

        """)
    filtered_df = df

    show_metrics(filtered_df, title="All India")

    # Crop share pie chart
    prod_by_crop = filtered_df.groupby("crop", as_index=False)["production"].sum()

    colg1, colg2 = st.columns(2)
    with colg1:
        fig = px.pie(
            prod_by_crop,
            values="production",
            names="crop",
            title="Share of Total Production by Crop",
            hole=0.3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Top states by yield
    with colg2:
        state_yield = (
            filtered_df.groupby("state", as_index=False)["yield"].mean()
            .sort_values(by="yield", ascending=False)
            .head(10)
        )
        fig = px.bar(
            state_yield,
            x="state",
            y="yield",
            title="Top 10 States by Average Yield",
            labels={"state": "State", "yield": "Average Yield (tons/ha)"},
            text_auto='.2f'
        )
        fig.update_traces(marker_color='green', textposition='outside')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


    # National yearly production
    yearly_production = filtered_df.groupby("year", as_index=False)["production"].sum()
    fig = px.line(
        yearly_production,
        x="year",
        y="production",
        title="Trend of Total Production Over Years",
        labels={"year": "Year", "production": "Total Production (tons)"},
        markers=True
    )
    fig.update_traces(line_color='blue', line_width=3)
    fig.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig, use_container_width=True)

    # National yield trend
    yield_trend = df.groupby("year", as_index=False)["yield"].mean()
    fig_yield_trend = px.line(
        yield_trend,
        x="year",
        y="yield",
        markers=True,
        title="📈 Average Yield Trend Over the Years",
        labels={"year": "Year", "yield": "Average Yield (tons/hectare)"},
    )
    fig_yield_trend.update_traces(line=dict(width=3), marker=dict(size=8))
    st.plotly_chart(fig_yield_trend, use_container_width=True)


    # If data has multiple states, aggregate to All India level
    india_df = filtered_df.groupby("year")[["area", "production"]].sum().reset_index()

    # Compute yield
    india_df["yield"] = india_df["production"] / india_df["area"]

    # ---- 1. Year-over-Year % Change in Production ----
    india_df["prod_pct_change"] = india_df["production"].pct_change() * 100

    fig1 = px.bar(
        india_df,
        x="year",
        y="prod_pct_change",
        title="Year-over-Year % Change in Agricultural Production (All India)",
        labels={"prod_pct_change": "% Change", "year": "Year"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ---- 2. Correlation Matrix ----
    corr = filtered_df[["area", "production", "yield"]].corr()

    fig2 = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Viridis",
        title="Correlation Matrix: Area, Production, Yield (All India)"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ---- 3. Bubble Chart ----
    fig3 = px.scatter(
        india_df,
        x="area",
        y="yield",
        size="production",
        color="year",
        hover_name="year",
        title="Yield vs Area (Bubble Size = Production, All India)",
        labels={"yield": "Yield (Production/Area)", "area": "Area (ha)"}
    )
    st.plotly_chart(fig3, use_container_width=True)


    #coconut crop analysis
    coconut_df = pd.read_csv("data/coconut_filtered.csv")

    # 1. Production trend over years
    st.subheader("📈 Coconut Production Trend Over Years")
    prod_year = coconut_df.groupby("year")["production"].sum().reset_index()
    fig1 = px.line(prod_year, x="year", y="production", markers=True,
                   title="Coconut Production Over the Years (All India)")
    st.plotly_chart(fig1, use_container_width=True)

    df_long = coconut_df.melt(
        id_vars="year",
        value_vars=["area", "production"],
        var_name="Metric",
        value_name="Value"
    )

    agg_df = coconut_df.groupby("year")[["area", "production"]].sum().reset_index()

    fig = px.line(
        agg_df,
        x="year",
        y=["area", "production"],
        markers=True,
        labels={"area": "Area (ha)", "production": "Production (tonnes)", "year": "Year"},
        title="Coconut Area vs Production (All India)"
    )

    # Set y-axis to log scale
    fig.update_yaxes(type="log")

    st.plotly_chart(fig, use_container_width=True)

    # 3. Yield trend
    st.subheader("📉 Yield Trend (Production / Area)")
    coconut_df["yield"] = coconut_df["production"] / coconut_df["area"]

    yield_year = coconut_df.groupby("year")["yield"].mean().reset_index()
    fig3 = px.line(yield_year, x="year", y="yield", markers=True,
                   title="Average Yield of Coconut Over Years")
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Season-wise share of production
    st.subheader("🗓️ Season-wise Share of Production")
    season_share = coconut_df.groupby("season")["production"].sum().reset_index()
    fig4 = px.pie(season_share, names="season", values="production",
                  title="Seasonal Share of Coconut Production")
    st.plotly_chart(fig4, use_container_width=True)

    # 5. Top states in coconut production
    st.subheader("🏆 Top States in Coconut Production")
    state_prod = coconut_df.groupby("state")["production"].sum().reset_index().sort_values(by="production",
                                                                                           ascending=False).head(10)
    fig5 = px.bar(state_prod, x="state", y="production", title="Top 10 States in Coconut Production")
    st.plotly_chart(fig5, use_container_width=True)

    # 6. Year & State filter for deeper analysis
    st.subheader("🔍 Filtered Analysis")
    year_filter = st.selectbox("Select Year", sorted(coconut_df["year"].unique()))
    state_filter = st.selectbox("Select State", sorted(coconut_df["state"].unique()))

    filtered_df = coconut_df[(coconut_df["year"] == year_filter) & (coconut_df["state"] == state_filter)]
    if not filtered_df.empty:
        st.write(f"Data for **{state_filter}** in **{year_filter}**")
        st.dataframe(filtered_df)
    else:
        st.warning("No data available for this selection.")

