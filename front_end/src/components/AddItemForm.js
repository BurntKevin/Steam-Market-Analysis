import React, { useState } from "react";
import { Form, Input, Button } from "semantic-ui-react";

export const AddItemForm = () => {
  const [itemName, setItemName] = useState("");

  return (
    <Form>
      <Form.Field>
        <Input
          placeholder="Add or update item by name"
          value={itemName}
          onChange={e => setItemName(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        <Button
          onClick={async () => {
            const item = { itemName };
            const response = await fetch("/add_item", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(item)
            });

            if (response.ok) {
              setItemName("");
            }
          }}
        >
          Submit
        </Button>
      </Form.Field>
    </Form>
  );
};

export default AddItemForm;
