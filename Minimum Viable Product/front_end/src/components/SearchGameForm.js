import React, { useState } from "react";
import { Form, Input, Button } from "semantic-ui-react";

function SearchGameForm() {
  const [gameName, setGameName] = useState([])

  return (
    <Form>
      <Form.Field>
        <Input
          placeholder="Search game by id"
          value={gameName}
          onChange={e => setGameName(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        <Button
          onClick={async () => {
            window.location.assign(
              "/view_game_items:".concat(gameName)
            )
          }}
        >
          Submit
        </Button>
      </Form.Field>
    </Form>
  );
}

export default SearchGameForm;