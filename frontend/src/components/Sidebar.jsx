import React, { useState } from "react";
import "../styles/Sidebar.css";
import DeleteIcon from "@mui/icons-material/Delete";


const Sidebar = ({ conversations, onAdd, onSelect, onDelete, activeConversation }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className={`sidebar ${isCollapsed ? "collapsed" : ""}`}>
      <div className="sidebar-header">
        {!isCollapsed && <h2>History</h2>}
        <button className="toggle-button" onClick={toggleSidebar}>
          {isCollapsed ? "→" : "←"}
        </button>
      </div>
      {!isCollapsed && (
        <>
          <ul>
            {conversations.map((conversation) => (
              <li
                key={conversation.id}
                className={`history-item ${
                  activeConversation === conversation.id ? "active" : ""
                }`}
                onClick={() => onSelect(conversation.id)}
              >
                <span className="conversation-name">{conversation.name}</span>
                <span
                  className="trash-icon"
                  onClick={(e) => {
                    e.stopPropagation(); // Prevent triggering `onSelect` when clicking the trash icon
                    onDelete(conversation.id);
                  }}
                >
                  <DeleteIcon
                style={{ fontSize: "20px", color: "gray" }}
                className="delete-icon"
              />
                </span>
              </li>
            ))}
          </ul>
          <button className="add-conversation" onClick={onAdd}>
            +
          </button>
        </>
      )}
    </div>
  );
};

export default Sidebar;
