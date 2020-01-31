import React, { useState } from "react";
import { Redirect } from 'react-router-dom';
import { Form, Input, Button } from "semantic-ui-react";
import axios from 'axios';

function SearchGameForm() {
  const [gameName, setGameName] = useState([])

  return (
    <Form>
      <Form.Field>
        <Input
          placeholder="Search game"
          value={gameName}
          onChange={e => setGameName(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        <Button
          onClick={async () => {
            window.location.assign(
              "/view_all_items:".concat(gameName)
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