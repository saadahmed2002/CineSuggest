import streamlit as st
import pickle
import pandas as pd
import difflib
import requests
from st_functions import st_button


st.markdown(
    """
<style>
.css-1wrcr25{
    background-image:url('https://springboard-cdn.appadvice.com/wp-content/appadvice-v2-media/2016/11/Netflix-background_860c8ece6b34fb4f43af02255ca8f225.jpg');
}
.e1tzin5v0{
    background:rgba(0,0,0,0.7);
    border-radius:0.6rem;
    gap: 50px;
    
}
.e1tzin5v0 p{
 
 margin: auto;
  width: 90%;
  
    
    text-color:white;
    gap: 50px;
   
}
.e1tzin5v0 button {
border-radius:0.1rem;
color:red;
background:color:blue;
}
.e1tzin5v0 button:hover {
border-radius:0.5rem;
color:red;
background:color:blue;
}
.e1tzin5v0 button p{
 
 margin: auto;
  width: 100%;
  
    font-weight:bold;
    text-color:white;
    gap: 50px;
   
}
.css-1y4p8pa{
padding:5rem;
max-width:80rem;
}

.css-5uatcg{
margin-left:40%;
margin-top:5%;
padding:1rem 4rem ;
}
#cinesuggest{
color:white;
padding:0.5;
margin-right:3rem;
margin-left:3rem;
text-decoration:underline;
border-radius:0.8rem 0rem 0rem 0.8rem;
background-color:rgba(255,255,230,0.4);

font-size:xxx-large;
}
.css-1r6slb0{
padding:5px;
border-radius:5px;
 background: repeating-linear-gradient(45deg, black, transparent 100px);
}
.e16nr0p30{
text-decoration:wavy;
}
.css-q8sbsg{
text-align:center;
 margin: auto;
  width: 50%;
  border-radius:7px;
  border: 3px solid white;
  padding: 10px;
}
.css-q8sbsg p{

   
    font-weight:bold;
    font-size:30px;
   
}
.st-au{
width:94%;
}
.st-c6{
padding:1rem;
}

.st-c6 p{

padding:1rem;

}
.stMarkdownContainer{
background:blue;
}
.e1tzin5v0 {
padding:2rem;
}
st-c8{
color:blue;
}
</style>
""",
    unsafe_allow_html=True,
)

def searchmovie(moviename):
  find_close_match = difflib.get_close_matches(moviename,list_of_all_titles)
  close_match = find_close_match[0]
  index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
  similarity_score = list(enumerate(similarity[index_of_the_movie]))
  sorted_similar_movies =   sorted(similarity_score,key = lambda x:x[1],reverse=True)
#   ------------------------
  recommendedmovies =[]
  recommendedmovies_poster = []
  recommendedmovies_link = []
  rating = []
  genres = []
  
# ========================
  i = 1
  for movie in sorted_similar_movies:
    index = movie[0]
    title_from_index =movies_data[movies_data.index == index]['title'].values[0]
    movie_id =movies_data[movies_data.index == index]['id'].values[0]
    gens = movies_data[movies_data.index == index]['genres'].values[0]
    if(i<13):   
      pics, link_url, rates = fetch_poster(movie_id)
      recommendedmovies_poster.append(pics)
      rating.append(rates)
      recommendedmovies_link.append(link_url)
      genres.append(gens)
      recommendedmovies.append(title_from_index)
      i+=1
  return recommendedmovies,recommendedmovies_poster,recommendedmovies_link,rating,genres;



def fetch_poster(movie_id):
  response =   requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b5d281f645eb0f41b823412b7e4f5850&language=en-US'.format(movie_id))
  data = response.json()
  
  pics = "http://image.tmdb.org/t/p/w500/"+data['poster_path']
  link_url = "https://www.imdb.com/title/"+data['imdb_id']
  ratings = data['vote_average']
  return pics,link_url,ratings


sorted_similar_movies = pickle.load(open('similarity.pkl',"rb"))
# movies_dict= pickle.load(open('movies_dict.pkl',"rb"))
movies_data= pickle.load(open('movies.pkl',"rb"))
list_of_all_titles= pickle.load(open('list_of_all_titles.pkl',"rb"))
similarity= pickle.load(open('similarities.pkl',"rb"))


t1 = "Welcome to CineSuggest, your ultimate destination for movie recommendations! Browse through our curated collection of films from various genres, including action, romance, comedy, and more, to find your next movie night pick."
text = "Discover the perfect movie for your mood with Movie Mania's personalized recommendations. "
text2 =t1 + text +"Our advanced algorithm takes into account your viewing history, preferences, and ratings to suggest movies tailored just for you, ensuring a delightful movie-watching experience every time."



st.write(' ')

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
text_input = st.text_input(
        "Enter MovieName/Genres/Tags...",
    )
st.title("CineSuggest")
st.write(text2)



def moviesfounds(names,posters,links,rates,gens):
   
   col1, col2, col3 = st.columns(3)
   with col1:
       st.image(posters[0])
    #    st.text("Genres: "+str(gens[0]))
       st.text("IMDB Rating: "+str(rates[0]))
       st_button(links[0], names[0])
       
       
   with col2:
       st.image(posters[1])
       st.text("IMDB Rating: "+str(rates[1]))
       st_button(links[1], names[1])
   
   with col3:
       st.image(posters[2])
       st.text("IMDB Rating: "+str(rates[2]))
       st_button(links[2], names[2])
   col1, col2, col3 = st.columns(3)
   with col1:
      st.image(posters[3])
      st.text("IMDB Rating: "+str(rates[3]))
      st_button(links[3], names[3])
      
   with col2:
       st.image(posters[4])
       st.text("IMDB Rating: "+str(rates[4]))
       st_button(links[4], names[4])
       
   with col3:
       st.image(posters[5])
       st_button(links[5], names[5])
       
   col1,col2,col3= st.columns(3)
   with col1:
       st.image(posters[6])
       st.text("IMDB Rating: "+str(rates[6]))
       st_button(links[6], names[6])
 
   
   with col2:
       st.image(posters[7])
       st.text("IMDB Rating: "+str(rates[7]))
       st_button(links[7], names[7])
   with col3:
      st.image(posters[8])
      st_button(links[8], names[8])
      st.text("IMDB Rating: "+str(rates[8]))
   col1,col2,col3= st.columns(3)
   with col1:
       st.image(posters[9])
       st.text("IMDB Rating: "+str(rates[9]))
       st_button(links[9], names[9])
 
   
   with col2:
       st.image(posters[10])
       st.text("IMDB Rating: "+str(rates[10]))
       st_button(links[10], names[10])
   with col3:
      st.image(posters[11])
      st.text("IMDB Rating: "+str(rates[11]))
      st_button(links[11], names[11])



if text_input:
    
    st.write('recommended movies')  
    names,posters,links,rating,gens = searchmovie(text_input)
    moviesfounds(names,posters,links,rating,gens)
    st.success("|^| Above ten movies are recommended movies.")



names,posters,links,rating,gens = searchmovie('marvels')
moviesfounds(names,posters,links,rating,gens)







footer="""<style>
body{
margin:0;
overflow-x:hidden;
}

.footer{
background:#000;
padding:30px 0px;
font-family: 'Play', sans-serif;
text-align:center;
}

.footer .row{
width:100%;
margin:1% 0%;
padding:0.6% 0%;
color:gray;
font-size:0.8em;
}

.footer .row a{
text-decoration:none;
color:gray;
transition:0.5s;
}

.footer .row a:hover{
color:#fff;
}

.footer .row ul{
width:100%;
}

.footer .row ul li{
display:inline-block;
margin:0px 30px;
}

.footer .row a i{
font-size:2em;
margin:0% 1%;
}

@media (max-width:720px){
.footer{
text-align:left;
padding:5%;
}
.footer .row ul li{
display:block;
margin:10px 0px;
text-align:left;
}
.footer .row a i{
margin:0% 3%;
}
}
</style>
<div class="footer">

<!--FONT AWESOME-->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

<!--GOOGLE FONTS-->
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Play&display=swap" rel="stylesheet"> 
</head>
<body>
<footer>
<div class="footer">
<div class="row">
<a href="#"><i class="fa fa-facebook"></i></a>
<a href="#"><i class="fa fa-instagram"></i></a>
<a href="#"><i class="fa fa-youtube"></i></a>
<a href="#"><i class="fa fa-twitter"></i></a>
</div>

<div class="row">
<ul>
<li><a href="#">Contact us</a></li>
<li><a href="#">Our Services</a></li>
<li><a href="#">Privacy Policy</a></li>
<li><a href="#">Terms & Conditions</a></li>
<li><a href="#">Career</a></li>
</ul>
</div>

<div class="row">All rights reserved || Designed By: Saad Ahmed 
</div>
</div>
</footer>

</div>
"""
st.markdown(footer,unsafe_allow_html=True)
