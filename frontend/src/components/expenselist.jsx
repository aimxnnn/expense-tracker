function ExpenseList({ exps, loaded }) {
  if (loaded === false) {
    return <p>Loading...</p>;
  }

  if (exps.length === 0) {
    return <p>You have no expenses yet.</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Amount</th>
          <th>Category</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        {exps.map((x) => (
          <tr key={x.id}>
            <td>{x.title}</td>
            <td>{x.amount}</td>
            <td>{x.category}</td>
            <td>{x.expense_date}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ExpenseList;
