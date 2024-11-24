const ChatBubble = ({ sender, text }) => {
  if (Array.isArray(text)) {
    return (
      <div className={`chat-bubble ${sender}`}>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Year</th>
              <th>Make</th>
              <th>Model</th>
              <th>Body</th>
              <th>Price</th>
              <th>Miles</th>
              <th>Color</th>
            </tr>
          </thead>
          <tbody>
            {text.map((car, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{car.Year}</td>
                <td>{car.Make}</td>
                <td>{car.Model}</td>
                <td>{car.Body}</td>
                <td>${car.SellingPrice}</td>
                <td>{car.Miles} ({car.Miles_Range})</td>
                <td>{car.Ext_Color_Generic}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  return <div className={`chat-bubble ${sender}`}>{text}</div>;
};
export default ChatBubble; // Default export
