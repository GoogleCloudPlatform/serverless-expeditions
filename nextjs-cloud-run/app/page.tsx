'use client'
import { useEffect, useState } from "react";
import { addFavoriteThing, getFavoriteThings } from "./actions";

export default function Home() {
  const [newFavoriteThing, setNewFavoriteThing] = useState('');
  const [favoriteThings, setFavoriteThings] = useState<string[]>([]);
  async function getThings() {
    const updatedListOfThings = await getFavoriteThings();
    setFavoriteThings(updatedListOfThings);
  }
  useEffect(() => {
    getThings();
  }, []);
  async function addThing() {
    await addFavoriteThing(newFavoriteThing);
    setNewFavoriteThing('');
    await getThings();
  }
  return (
    <main>
      <h1>Hello Martin!</h1>
      <h2>Luke&apos;s Favorite Things</h2>
      <input
        placeholder="New Favorite Thing"
        value={newFavoriteThing}
        onChange={(e) => setNewFavoriteThing(e.target.value)}
        className="border-black border-2"
      />
      <button onClick={addThing} className="border-black border-2 hover:text-white hover:bg-black rounded">
        Add Favorite Thing
      </button>
      <ul className="list-disc list-inside">
        {favoriteThings.map(function (thing) {
          return <li key={thing}>{thing}</li>
        })}
      </ul>
    </main>
  );
}
