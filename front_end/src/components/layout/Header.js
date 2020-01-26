import React, { useEffect, useState } from "react";
import { Input, Menu, Item } from 'semantic-ui-react'
import AddGameForm from '../AddGameForm';

function Header() {
  const [games, setGames] = useState([]);

  useEffect(() => {
    fetch("/games").then(response =>
      response.json().then(data => {
        setGames(data.games);
      })
    );
  }, []);

  return (
    <Menu stackable>
      <Menu.Item href="/">
        <Item.Image src="favicon.ico" size="tiny"/>
      </Menu.Item>

      <Menu.Item>
        <AddGameForm
          onNewGame={game =>
            setGames(currentGames => [game])
          }
        />
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
