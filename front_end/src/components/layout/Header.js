import React from "react";
import { Menu, Item } from 'semantic-ui-react'
import AddGameForm from '../AddGameForm';
import SearchGameForm from '../SearchGameForm';
import SearchItemForm from '../SearchItemForm';

function Header() {
  return (
    <Menu stackable>
      <Menu.Item href="/">
        <Item.Image src="favicon.ico" size="tiny"/>
      </Menu.Item>

      <Menu.Item>
        <AddGameForm/>
      </Menu.Item>

      <Menu.Item position='right'>
        <SearchGameForm/>
        <SearchItemForm/>
      </Menu.Item>
    </Menu>
  );
}

export default Header;
