import React from 'react'
import PropTypes from 'prop-types'

require('./DropdownLang.styl')

const DropdownLang = props => {
  const activeLang = props.langList.find(l => l.id === props.idLangActive)
  return (
    <li className='header__menu__rightside__itemlanguage'>
      <div className='header__menu__rightside__itemlanguage__languagedropdown dropdown'>
        <button
          type='button'
          className='languagedropdown__btnlanguage btn outlineTextBtn nohover primaryColorBorder dropdown-toggle'
          id='headerDropdownMenuButton'
          data-toggle='dropdown'
          aria-haspopup='true'
          aria-expanded='false'
        >
          <img className='languagedropdown__btnlanguage__imgselected' src={activeLang.icon} />
          { activeLang.label }
        </button>
        <div className='languagedropdown__subdropdown dropdown-menu' aria-labelledby='headerDropdownMenuButton'>
          { props.langList.filter(l => l.id !== props.idLangActive).map(l =>
            <div className='subdropdown__link primaryColorBgLightenHover dropdown-item' onClick={() => props.onChangeLang(l.id)} key={l.id}>
              <img className='subdropdown__flag mr-2' src={l.icon} />
              { l.label }
            </div>
          )}
        </div>
      </div>
    </li>
  )
}
export default DropdownLang

DropdownLang.propTypes = {
  langList: PropTypes.array.isRequired,
  idLangActive: PropTypes.string.isRequired,
  onChangeLang: PropTypes.func.isRequired
}
