import React, { useState } from "react";
import { Form, Input, Button } from "semantic-ui-react";

export const AddGameForm = () => {
  const [gameId, setGameId] = useState("");

  return (
    <Form>
      <Form.Field>
        <Input
          placeholder="Add or update game by id"
          value={gameId}
          onChange={e => setGameId(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        <Button
          onClick={async () => {
            const game = { gameId };
            alert("Sending request to add game, allow about 3 seconds of processing per item");
            const response = await fetch("https://analysis-back-end.herokuapp.com/add_game", {
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
