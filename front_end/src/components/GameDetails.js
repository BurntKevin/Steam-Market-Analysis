import React from "react";
import { List, Header } from "semantic-ui-react";

export const GameDetails = ({ games }) => {
  return (
    <List>
      {
        "GameDetails"
        /* {games.map(game => {
        return (
          <List.Item key={game.id}>
            <Header>{game.id}</Header>
          </List.Item>
        );
      })} */}
    </List>
  );
};
