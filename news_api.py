from flask import Flask, Blueprint, jsonify, make_response, request
from data import db_session
from data.users import User
from data.news import News

app = Flask(__name__)
blueprint = Blueprint('news_api', __name__,
                            template_folder='templates')

@blueprint.route('/api/news')
def get_news():
    session = db_session.create_session()
    news = session.query(News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in news]
        }
    )


@blueprint.route('/api/news/<int:news_id>',  methods=['GET'])
def get_one_news(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': news.to_dict(only=('title', 'content', 'user_id', 'is_private'))
        }
    )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private', 'is_published']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    news = News(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private'],
        is_published=request.json['is_published']
    )
    session.add(news)
    session.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    session.delete(news)
    session.commit()
    return jsonify({'success': 'OK'})