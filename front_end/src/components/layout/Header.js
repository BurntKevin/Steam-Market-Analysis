import React, { useEffect, useState } from "react";
import { Input, Menu, Item } from 'semantic-ui-react'
import GameForm from '../AddGameForm';

function Header() {
  return (
    <Menu stackable>
      <Menu.Item href="/">
        <Item.Image src="favicon.ico" size="tiny"/>
      </Menu.Item>

      <Menu.Item>
        <GameForm/>
      </Menu.Item>

      <Menu.Item position='right'>
        <Input
          action={{ type: 'submit', content: 'Go' }}
          placeholder='Search game'
        />

        <Input
          action={{ type: 'submit', content: 'Go' }}
          placeholder='Search item'
        />
      </Menu.Item>
    </Menu>
  );
}

export default Header;
