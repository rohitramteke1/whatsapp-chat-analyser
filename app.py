import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("📂 Upload Chat")

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file (.txt)")
st.sidebar.markdown("💡 *Upload the exported `chat.txt` file*")

# 📄 Landing Page
if uploaded_file is None:
    st.title("📊 WhatsApp Chat Analyzer")

    st.markdown("""
    Welcome to the **WhatsApp Chat Analyzer**! 📱💬  
    This tool helps you explore and visualize your WhatsApp conversations with insightful stats and charts.

    ---

    ### 🧭 How to Use:
    1. **Export a WhatsApp Chat**:
       - Open any WhatsApp chat  
       - Tap the 3-dot menu → **More** → **Export Chat** → Choose **Without Media**
    2. **Save the file as** `chat.txt`.
    3. **Upload the file** using the sidebar on the left.
    4. **Select a user** (or "Overall") and click **Show Analysis** to get:
       - 📈 Message and word stats  
       - 📆 Activity over time  
       - 🔥 Busiest days/months  
       - ☁️ Wordcloud and common words  
       - 😄 Emoji analysis  
       - 👥 Most active users (for group chats)

    ---

    ### 📝 Notes:
    - Works best with English-language WhatsApp exports.
    - Only `.txt` file format is supported.
    - File name should be `chat.txt` for consistency (recommended).

    ---

    ### 👨‍💻 Created by [rohitramteke1](https://github.com/rohitramteke1)
    """)
else:
    # Read file and preprocess
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(heatmap, ax=ax)
        st.pyplot(fig)

        # Group Chat Analysis
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.dataframe(new_df)

            st.title("User Contribution Pie Chart")
            fig, ax = plt.subplots()
            ax.pie(x.values, labels=x.index, autopct='%1.1f%%')
            st.pyplot(fig)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # Most Common Words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = helper.analyze_emojis(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)
