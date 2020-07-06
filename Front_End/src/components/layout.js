import React from "react";
import { Menu,  Container, Image } from "semantic-ui-react";

function Layout({ body }) {
  return (
    <Container fluid>
      <Menu stackable>
        <Image src="logo.png" size="mini" />
      </Menu>

      <Container fluid>
        {body}
      </Container>
    </Container>
  );
}

export default Layout;
