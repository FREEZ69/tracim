import React from 'react'
import classnames from 'classnames'

const Thread = props => {
  return (
    <div className='wsContentThread__app'>
      <ul className='wsContentThread__app__messagelist wsContentGeneric__messagelist'>
        { props.listMessage.map(msg =>
          <li className={classnames('wsContentThread__app__messagelist__item', 'wsContentGeneric__messagelist__item', {
            'sended': props.loggedUser.id === msg.author.id,
            'received': !(props.loggedUser.id === msg.author.id)
          })} key={msg.id}>
            <div className='wsContentThread__app__messagelist__item__avatar wsContentGeneric__messagelist__item__avatar'>
              <img src={msg.author.avatar} alt='avatar' />
            </div>

            <div className='wsContentThread__app__messagelist__item__createhour wsContentGeneric__messagelist__item__createhour'>
              {msg.createdAt.day} à {msg.createdAt.hour}
            </div>

            <div className='wsContentThread__app__messagelist__item__content wsContentGeneric__messagelist__item__content'>
              {msg.text}
            </div>
          </li>
        )}
      </ul>

      <form className='wsContentThread__app__texteditor wsContentGeneric__texteditor'>
        <div className='wsContentThread__app__texteditor__simpletext wsContentGeneric__texteditor__simpletext input-group'>
          <input type='text' className='wsContentThread__app__texteditor__simpletext__input wsContentGeneric__texteditor__simpletext__input form-control' placeholder='...' />

          <div className='wsContentThread__app__texteditor__simpletext__icon wsContentGeneric__texteditor__simpletext__icon input-group-addon'>
            <i className='fa fa-font' />
          </div>
        </div>

        <div className='wsContentGeneric__texteditor__wysiwyg d-none d-xl-block'>
          <textarea />
        </div>

        <div className='wsContentThread__app__texteditor__submit wsContentGeneric__texteditor__submit d-xl-flex justify-content-xl-center'>
          <button type='submit' className='wsContentThread__app__texteditor__submit__btn wsContentGeneric__texteditor__submit__btn btn btn-primary'>
            Envoyer
            <div className='wsContentThread__app__texteditor__submit__btn__icon wsContentGeneric__texteditor__submit__btn__icon'>
              <i className='fa fa-paper-plane-o' />
            </div>
          </button>
        </div>
      </form>
    </div>
  )
}

export default Thread
