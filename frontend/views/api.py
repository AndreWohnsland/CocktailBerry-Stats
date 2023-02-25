import streamlit as st


def api_guidelines():
    """Shows the needed information to get the API key for CocktailBerry"""
    st.header("❓ How to participate")
    st.markdown(
        """
        The tl;dr is you need to build your own [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry)
        machine and install the software on it. After that, you [provide me proof](mailto:cocktailmakeraw@gmail.com)
        that it exists / works  (video / pictures / blog or social media post).
        Afterwards, you will get an API key to submit your machine data.
        """)
    with st.expander("Show details and reasons behind them:"):
        _detailed_explanation()


def _detailed_explanation():
    st.markdown(
        """
        #### How To

        The current procedure require you to build your own **CocktailBerry** machine and deliver some kind of proof of its existence.
        The easiest way to do this is to submit a video or some photos of your machine.
        The machine does **NOT** need to be fancy in any way, it should simply work, be able to make cocktails
        and run the CocktailBerry software.
        It does not matter if the pumps are showing or the cabling looks like a mess. 😉

        Please upload your video / photos to some sort of hosting site (Imgur, etc.) and provide the link,
        or give a reference to your blog post (own blog, Reddit, social media) if you did such things for your machine.
        It would be nice to write some words in addition to the submission, even if it's just a kind greeting,
        and provide me some sort of name or alias how should I reply to you (first name or your preferred alias is fine).
        You can [contact me](mailto:cocktailmakeraw@gmail.com) for further questions or just to get the API-key.

        #### Why a Protected API

        The reason behind this is that only **real machines** should submit data for the dashboard (you could otherwise
        just run the Python program anywhere and submit a lot of data) and to minimize any other kinds of exploits
        of the API. There is no option to submit a photo (the implementation here would be quite simple) because this could
        also be exploited quite easily. The internet is still a wild and scary place! 🦖
        Also, I would love to see what you did in combination with my software.

        #### Final Steps

        You can then use the received API key for the CocktailBerry microservice (in the .env file).
        As soon as there is a valid key and the microservice is enabled, your machine will send the cocktail data
        (*cocktail name, machine name, volume and language setting*) to the API using the API-key.
        The activation of this feature is also explained in the CocktailBerry docs.

        #### Will this be Easier in the Future

        I always work on improvements and try to bring the most joy with CocktailBerry and related projects.
        Since I do it all in my free time + open source, sadly my time is limited, and I can only do so much.
        If you may know a better way, feel free to contact me and let's start a nice discussion to make the
        CocktailBerry environment even better!
        """
    )
