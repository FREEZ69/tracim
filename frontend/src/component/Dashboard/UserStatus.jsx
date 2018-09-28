import React from 'react'
import {ROLE} from '../../helper.js'

require('./UserStatus.styl')

// @TODO Côme - 2018/08/07 - since api yet doesn't handle notification subscriptions, this file is WIP
export const UserStatus = props => {
  const mySelf = props.curWs.memberList.find(m => m.id === props.user.user_id) || {role: ''}
  const myRole = ROLE.find(r => r.slug === mySelf.role) || {faIcon: '', hexcolor: '', label: ''}

  return (
    <div className='userstatus notched primaryColorBorder'>
      <div className='userstatus__username'>
        {props.user.public_name}
      </div>

      <div className='userstatus__role'>
        <div className='d-flex align-items-center'>
          <div className='userstatus__role__icon'>
            <i className={`fa fa-fw fa-${myRole.faIcon}`} style={{color: myRole.hexcolor}} />
          </div>

          <div
            className='userstatus__role__text ml-3'
            title={props.t('your role in the shared space')}
            style={{color: myRole.hexcolor}}
          >
            {props.t(myRole.label)}
          </div>
        </div>
      </div>

      <div
        className='userstatus__notification primaryColorFontHover'
        onClick={mySelf.doNotify ? props.onClickRemoveNotify : props.onClickAddNotify}
      >
        <div className='userstatus__notification__icon'>
          <i className={`fa fa-fw fa-envelope${mySelf.doNotify ? '-open' : ''}-o`} />
        </div>

        <div
          className='userstatus__notification__text ml-3'
          title={props.t('you can change your notification status by clicking here')}
        >
          {mySelf.doNotify
            ? props.t('Subscribed to the notifications')
            : props.t('Unsubscribed to the notifications')
          }
        </div>
      </div>
    </div>
  )
}

export default UserStatus
