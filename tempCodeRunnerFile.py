st.markdown("<h1 style='text-align: center; color: white;'>💹 TijoriTrends: Binance Beacon 🌟</h1>", unsafe_allow_html=True)
    st.image("https://media.tenor.com/T-zDRVK4XdQAAAAd/tradinggif.gif")
    
    st.markdown("<h1 style='text-align: center; color: white;'>💹 TijoriTrends: Binance Beacon 🌟</h1>", unsafe_allow_html=True)
    
    # Load the GIF image from the URL
    gif_url = "https://media.tenor.com/zzntm2_9B3gAAAAC/hacker.gif"
    gif_image = Image.open(requests.get(gif_url, stream=True).raw)
    
    # Apply a blur filter to the GIF image
    blurred_gif = gif_image.filter(ImageFilter.BLUR)
    
    # Display the blurred GIF image
    st.image(blurred_gif, caption="Blurred GIF Image")