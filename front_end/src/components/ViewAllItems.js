import React, { useEffect, useState } from "react";
import { Card, Image } from "semantic-ui-react";
import axios from 'axios';

export const ViewAllItems = ({ game_id }) => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    axios
    .get("/view_all_items", {
      params: {
        game_id,
      },
    })
    .then(({ data }) => {
      setItems(data.items);
    })
  }, []);

  return (
    <Card.Group itemsPerRow={5}>
      {items.map(item => {
        return (
          <Card href={"/view_item_analysis:" + item.item_name}>
            <Image src={item.item_icon} wrapped ui={false} />
            <Card.Content>
              <Card.Header>{item.item_name}</Card.Header>
            </Card.Content>
          </Card>
        );
      })}
    </Card.Group>
  );
};

export default ViewAllItems;
