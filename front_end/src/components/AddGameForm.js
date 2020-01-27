import React, { useState } from "react";
import { Form, Input, Button } from "semantic-ui-react";

export const AddGameForm = ({ onNewGame }) => {
  const [gameId, setGameId] = useState("");

  return (
    <Form>
      <Form.Field>
        <Input
          placeholder="Add game by id"
          value={gameId}
          onChange={e => setGameId(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        <Button
          onClick={async () => {
            const game = { gameId };
            const response = await fetch("/add_game", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(game)
            });

            if (response.ok) {
              setGameId("");
            }
          }}
        >
          Submit
        </Button>
      </Form.Field>
    </Form>
  );
};

export default AddGameForm;
