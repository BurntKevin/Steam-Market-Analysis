import React from 'react';
import { Container } from "semantic-ui-react";
import Layout from "../components/layout/index";

function HomePage(props) {
  return (
    <Layout
        body="Body"
    />
  );
}

export default HomePage;


// import React, { useEffect, useState } from "react";
// import { GameDetails } from "../components/GameDetails";
// import { Container } from "semantic-ui-react";
// import { GameForm } from "../components/GameForm";

// function ViewGamePage({game}) {
//     const [games, setGames] = useState([]);

//     return (
//       <Container style={{ marginTop: 40 }}>
//         <GameDetails games={games} />
//       </Container>
//     );
// }

// export default ViewGamePage;

