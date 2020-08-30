import React, { useState } from "react";
import { Form, Input, Button } from "semantic-ui-react";

function SearchItemForm() {
  const [itemName, setItemName] = useState([])

  return (
    <Form>
      <Form.Field>
        <Input
          placeholder="Search item by name"
          value={itemName}
          onChange={e => setItemName(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        <Button
          onClick={async () => {
            window.location.assign(
              "/view_item_analysis:".concat(itemName)
            )
          }}
        >
          Submit
        </Button>
      </Form.Field>
    </Form>
  );
}

export default SearchItemForm;