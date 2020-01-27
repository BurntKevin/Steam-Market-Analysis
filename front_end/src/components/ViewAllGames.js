import React, { useEffect, useState } from "react";
import { Card, Image } from "semantic-ui-react";

export const ViewAllGames = () => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    fetch("/basic_game_data").then(response =>
      response.json().then(data => {
        setGames(data.games);
      })
    );
  }, []);

  return (
    <Card.Group itemsPerRow={5}>
      {games.map(game => {
        return (
          <Card href={"view_all_items:" + game.game_id}>
            <Image src={game.game_icon} wrapped ui={false} />
            <Card.Content>
              <Card.Header>{game.game_id}</Card.Header>
            </Card.Content>
          </Card>
        );
      })}
    </Card.Group>
  );
};

export default ViewAllGames;
