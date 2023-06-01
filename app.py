from flask import Flask,render_template,request
import pandas as pd
import numpy as np
top_50=pd.read_pickle(open('top50.pkl', 'rb'))
books=pd.read_pickle(open('books.pkl', 'rb'))
pt=pd.read_pickle(open('pt.pkl', 'rb'))
similarity=pd.read_pickle(open('similarity.pkl','rb'))
app=Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html",
                           book_name=list(top_50['Book-Title'].values),
                           #to get only the values of books instead of whole colmn we convert into umpy array using values and for ease of access we convert it to list
                           author=list(top_50['Book-Author'].values),
                           votes=list(top_50['No_of_votes'].values),
                           avg_rating = list(top_50['Avg Rating'].values),
                           image = list(top_50['Image-URL-M'].values)
                           )
@app.route("/about")
def about():
    return render_template("about.html")
@app.route('/recommendation')
def recommender():
    return render_template('recommendation.html')
@app.route('/recommender1',methods=['GET','POST'])
# upgraded version of recommend function
def recommend():
    try:
        book_name=request.args['book_title']
        index = np.where(pt.index.str.lower() == book_name.lower())[0][0]
    except:
        return render_template('recommendation.html',
                               str1="No Recommendations Available Currently")
    distances = similarity[index]
    similar_items = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    # print(similar_items)
    data = []
    for i in similar_items:
        # print(pt.index[i[0]])
        items = []
        temp = books[books['Book-Title'] == pt.index[i[0]]]
        items.extend(temp.drop_duplicates('Book-Title')['Book-Title'])
        items.extend(temp.drop_duplicates('Book-Title')['Book-Author'])
        items.extend(temp.drop_duplicates('Book-Title')['Image-URL-M'])
        data.append(items)
    print(data)
    return render_template('recommendation.html',
                           data=data)
    # return the title which is similar to the index number that we got from similar items
    # return suggestions
    #return the title which is similar to the index number that we got from similar items
    #return suggestions
@app.route('/loaderio-0339159fc8af6f665c03aa5f82f15e04.txt')  
def test():
    return send_file('loaderio-0339159fc8af6f665c03aa5f82f15e04.txt')
if __name__=='__main__':
    app.run(debug=True)
